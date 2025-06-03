from rest_framework import serializers
from .models import GoogleUser, Chat, ChatMessage


class UserSerializer(serializers.ModelSerializer):  # Use ModelSerializer instead
    class Meta:
        model = GoogleUser
        fields = ["google_id", "email", "name", "picture"]


class LimitedChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["title", "updated_at","chat_id"]  # Include only required fields


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = [
            "question",
            "answer",
            "created_at",
            "lnode",
            "urls",
            "code",
            "code_instruction",
        ]  # Include relevant fields for messages
