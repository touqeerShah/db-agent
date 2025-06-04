from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.core.cache import cache
import time
import asyncio

from asgiref.sync import sync_to_async, async_to_sync  # Needed for async compatibility
from google.auth.transport.requests import Request
from langchain_core.messages import HumanMessage, AIMessage

from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.exceptions import NotFound, AuthenticationFailed

from rest_framework import status

from rest_framework.decorators import api_view
from .models import GoogleUser
from .serializers import UserSerializer
import json
from django.http import StreamingHttpResponse, JsonResponse, HttpRequest
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .llm_agent.agent import Agent
from .llm_agent.helper import IntentResponse, SQLResponse
from typing import List, Dict, Any

from django.http import StreamingHttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from api.utils.chat_utils import create_chat, get_user_chats_paginated
from .serializers import LimitedChatSerializer, ChatMessageSerializer
from .models import Chat, ChatMessage

import json


@method_decorator(csrf_exempt, name="dispatch")
class ReportGenerationView(View):
    def get(self, request, chat_id):
        try:
            # Step 1: Extract and validate query parameters
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise AuthenticationFailed("Authorization header missing or malformed.")

            id_token = auth_header.split(" ")[1]
            query = request.GET.get("query")
            collections = json.loads(request.GET.get("collections", "[]"))

            # Step 2: Perform JWT verification
            verification_result, status_code = asyncio.run(
                _verify_google_token(id_token, request)
            )
            if not verification_result.get("isLogin"):
                return JsonResponse(verification_result, status=status_code)

            # Step 3: Initialize Agent and AgentState with extracted parameters
            timestamp = str(time.time())
            user_id = verification_result.get("user", {}).get("google_id")
            # chat_id = generate_unique_hash(chat_id + user_id + timestamp)

            agent_state_data = {
                "query":query,
                "chat_id":chat_id,
                "sql_response": SQLResponse(is_allow=False, query=[]),
                "intent_classification": IntentResponse(intent="store_info"),
                "role": "admin",  # or "admin", "employee"
                "collection_names": ["store_info"],
                "summary": "",
                "answer":""
            }
            # print("agent_state_data :  ", agent_state_data)
            google_user, created = GoogleUser.objects.get_or_create(
                google_id=user_id,
                defaults={
                    "email": verification_result["user"].get("email"),
                    "name": verification_result["user"].get("name"),
                    "picture": verification_result["user"].get("picture"),
                },
            )
            create_chat(chat_id, google_user=google_user, question=query)
            # Reconstruct report from collections
            report = Agent(collections, "llama-pro:8b-instruct-q5_K_M")
            final_message = {}

            # Step 4: Define synchronous generator for SSE
            def generator_wrapper():
                async def fetch_chunks():
                    async for chunk in report.report_stream(agent_state_data, chat_id):
                        final_message = chunk
                        response = json.dumps(
                            {"status": "Processing", "message": chunk}
                        )
                        yield f"data: {response}\n\n"

                        # await asyncio.sleep(0.1)  # Simulate live streaming delay
                    final_message_serialized = json.dumps(
                        {"status": "Done", "message": final_message}
                    )  # Convert the entire message to JSON

                    # Yield the serialized JSON with newline characters formatted for SSE
                    yield f"data: {final_message_serialized}\n\n"
                    # yield f'data: {"status": "Done","message":{json.dumps(final_message)}}\n\n'

                # Run async generator synchronously
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                async_gen = fetch_chunks()
                try:
                    while True:
                        chunk = loop.run_until_complete(async_gen.__anext__())
                        yield chunk
                except StopAsyncIteration:
                    pass
                finally:
                    loop.close()

            response = StreamingHttpResponse(
                generator_wrapper(),
                content_type="text/event-stream",
            )

            # Set required headers for SSE, excluding 'Connection: keep-alive'
            response["Cache-Control"] = "no-cache"
            response["X-Accel-Buffering"] = "no"  # For some reverse proxies like Nginx

            # Optional: Set CORS headers if necessary
            response["Access-Control-Allow-Origin"] = (
                "*"  # Replace '*' with specific origin if needed
            )

            return response

        except Exception as e:
            print(f"Unexpected error in ReportGenerationView get method: {e}")
            return JsonResponse(
                {"detail": "Unexpected internal server error"}, status=500
            )


class ListChatView(APIView):
    def get(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Authorization header missing or malformed.")

        id_token = auth_header.split(" ")[1]
        verification_result, _ = async_to_sync(_verify_google_token)(id_token, request)

        if not verification_result.get("isLogin"):
            raise AuthenticationFailed("JWT verification failed.")

        user_id = verification_result.get("user", {}).get("google_id")
        if not user_id:
            raise AuthenticationFailed("User ID not found in token.")

        page = int(request.GET.get("page", 1))
        per_page = int(request.GET.get("per_page", 20))

        paginated_data = get_user_chats_paginated(user_id, page, per_page)
        return Response(paginated_data)

@method_decorator(csrf_exempt, name="dispatch")
class ChatMessagesView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        request = self.request
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Authorization header missing or malformed.")

        id_token = auth_header.split(" ")[1]
        chat_id = self.kwargs.get("chat_id")

        verification_result, status_code = async_to_sync(_verify_google_token)(
            id_token, request
        )
        if not verification_result.get("isLogin"):
            raise AuthenticationFailed("JWT verification failed.")

        # ✅ Return actual model instances here
        return ChatMessage.objects.filter(chat__chat_id=chat_id).order_by("created_at")

@method_decorator(csrf_exempt, name="dispatch")
class ChatDeleteView(generics.DestroyAPIView):
    permission_classes = [AllowAny]  # Set permissions as per your requirements

    def get_object(self):
        request = self.request
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Authorization header missing or malformed.")

        id_token = auth_header.split(" ")[1]
        chat_id = self.kwargs.get("chat_id")  # Retrieve chat_id from URL parameters

        # Step 1: Perform JWT verification
        verification_result, status_code = async_to_sync(_verify_google_token)(
            id_token, request
        )
        if not verification_result.get("isLogin"):
            raise AuthenticationFailed("JWT verification failed. User not logged in.")

        # Step 2: Retrieve Google user ID from verification result
        user_id = verification_result.get("user", {}).get("google_id")
        if not user_id:
            raise AuthenticationFailed("Invalid token: User ID not found.")

        # Step 3: Check if the specified chat exists for this user
        try:
            chat = Chat.objects.get(chat_id=chat_id, google_user__google_id=user_id)
        except Chat.DoesNotExist:
            raise NotFound("Chat not found for this user.")

        return chat

    def delete(self, request, *args, **kwargs):
        chat = self.get_object()
        chat.delete()
        return Response(
            {"detail": "Chat deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


@api_view(["GET"])
def get_user_details(request, google_id):
    """Retrieve user details by google_id."""
    try:
        user = GoogleUser.objects.get(google_id=google_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except GoogleUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def create_user(request):
    print("Request Path:", request.path)
    """Create or get a Google user based on ID."""
    data = request.data
    google_id = data.get("google_id")

    if not google_id:
        return Response({"error": "Missing google_id"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if user already exists
    user, created = GoogleUser.objects.get_or_create(google_id=google_id, defaults=data)
    if not created:
        # If exists, optionally update the other fields
        for field, value in data.items():
            setattr(user, field, value)
        user.save()

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def verify_google_token(request):
    token = request.data.get("idToken")
    # print(token)
    if not token:
        return Response(
            {"isLogin": False, "googleId": None, "message": "Token is missing"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        # Verify the token synchronously
        verification_result, status_code = async_to_sync(_verify_google_token)(
            token, request
        )

        return Response(verification_result, status=status_code)

    except ValueError:
        # Invalid token
        return Response(
            {"isLogin": False, "googleId": None, "message": "Invalid token"},
            status=status.HTTP_400_BAD_REQUEST,
        )


async def _verify_google_token(token, request):
    if not token:
        return {
            "isLogin": False,
            "googleId": None,
            "message": "Token is missing",
        }, status.HTTP_401_UNAUTHORIZED  # Use 401 for missing token

    try:
        # Use sync_to_async to run the token verification in a synchronous context
        id_info = await sync_to_async(id_token.verify_oauth2_token)(
            token, Request(), settings.GOOGLE_CLIENT_ID
        )

        # Extract user information
        google_id = id_info["sub"]
        email = id_info["email"]
        name = id_info["name"]
        picture = id_info.get("picture")

        # Check if user exists or create a new one
        user, created = await sync_to_async(GoogleUser.objects.get_or_create)(
            google_id=google_id,
            defaults={"email": email, "name": name, "picture": picture},
        )

        # Update user details if user already exists
        if not created:
            user.email = email
            user.name = name
            user.picture = picture
            await sync_to_async(user.save)()

        # Serialize user data
        serializer = UserSerializer(user, context={"request": request})
        return {
            "isLogin": True,
            "isVerify": True,
            "user": serializer.data,
        }, status.HTTP_200_OK

    except ValueError:
        # Invalid token
        return {
            "isLogin": False,
            "googleId": None,
            "message": "Invalid token",
        }, status.HTTP_401_UNAUTHORIZED  # Use 401 for invalid token
