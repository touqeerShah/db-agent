from django.core.paginator import Paginator

from typing import Optional, Dict, Any
from django.core.exceptions import ObjectDoesNotExist
from api.models import Chat, ChatMessage, GoogleUser

from api.serializers import LimitedChatSerializer,ChatMessageSerializer,ChatMessageSerializer
def create_chat(
    chat_id: str, google_user: GoogleUser, question: str
) -> Chat:
    chat, created = Chat.objects.get_or_create(
        chat_id=chat_id,
        defaults={
            "google_user": google_user,
            "title": question[:64],
        },
    )
    # if created:
    #     ChatMessage.objects.create(chat=chat, question=question)
    return chat

def create_chat_message(
    chat_id: str,
    question: str = "",
    answer: str = "",
    intent_classification: Dict[str, Any] = None,
    sql_response: Dict[str, Any] = None,
) -> ChatMessage:
    chat = Chat.objects.get(chat_id=chat_id)
    return ChatMessage.objects.create(
        chat=chat,
        question=question,
        answer=answer,
        intent_classification=intent_classification or {},
        sql_response=sql_response or {},
    )


def update_chat_summary(chat_id: str, summary: str) -> ChatMessage:
    chat = Chat.objects.get(chat_id=chat_id)

    chat.summary = summary
    chat.save()
    return chat

def update_chat_lnode(chat_id: str, lnode: str) -> ChatMessage:
    chat = Chat.objects.get(chat_id=chat_id)

    chat.lnode = lnode
    chat.save()
    return chat

def get_chat_summary(chat_id: str, ) -> ChatMessage:
    chat = Chat.objects.get(chat_id=chat_id)
    return chat.summary


def get_last_chat_message(chat_id: str) -> Optional[Dict[str, str]]:
    try:
        chat = Chat.objects.get(chat_id=chat_id)
        message = chat.messages.last()
        if message:
            return {
                "question": message.question,
                "answer": message.answer,
            }
        return None
    except Chat.DoesNotExist:
        return None



def get_user_chats_paginated(user_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """Return paginated list of chats for a user."""
    chats = Chat.objects.filter(google_user__google_id=user_id).order_by('-updated_at')
    paginator = Paginator(chats, per_page)
    page_obj = paginator.get_page(page)

    serializer = LimitedChatSerializer(page_obj.object_list, many=True)


    return {
        "results": serializer.data,
        "current_page": page,
        "total_pages": paginator.num_pages,
        "total_chats": paginator.count,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
    }
def get_chat_details(chat_id: str) -> Dict[str, Any]:
    """Return full chat details including messages."""
    try:
        chat = Chat.objects.get(chat_id=chat_id)
        messages = chat.messages.all().order_by("created_at")

        return {
            "chat_id": chat.chat_id,
            "title": chat.title,
            "created_at": chat.created_at,
            "updated_at": chat.updated_at,
            "summary": getattr(chat, "summary", None),
            "collection": chat.collection,
            "messages": ChatMessageSerializer(messages, many=True).data,
        }

    except Chat.DoesNotExist:
        return {"error": "Chat not found"}