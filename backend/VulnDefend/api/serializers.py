from rest_framework import serializers
from .models import GoogleUser, Chat, ChatMessage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleUser
        fields = ["google_id", "email", "name", "picture", "role"]


class LimitedChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["title", "updated_at", "chat_id"]


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = [
            "question",
            "answer",
            "created_at",
            "intent_classification",
            "sql_response",
        ]
