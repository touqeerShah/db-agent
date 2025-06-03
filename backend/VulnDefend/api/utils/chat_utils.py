from django.core.paginator import Paginator

from typing import Optional, Dict, Any
from django.core.exceptions import ObjectDoesNotExist
from api.models import Chat, ChatMessage, GoogleUser


def create_chat(
    chat_id: str, title: str, google_user: GoogleUser, question: str
) -> Chat:
    chat, created = Chat.objects.get_or_create(
        chat_id=chat_id,
        defaults={
            "google_user": google_user,
            "title": question[:64],
        },
    )
    if created:
        ChatMessage.objects.create(chat=chat, question=question)
    return chat


def update_chat_intent(chat_id: str, intent_data: Dict[str, Any]) -> ChatMessage:
    chat = Chat.objects.get(chat_id=chat_id)
    message = chat.messages.last()
    message.intent_classification = intent_data
    message.save()
    return message


def update_chat_sql_response(chat_id: str, sql_response: Dict[str, Any]) -> ChatMessage:
    chat = Chat.objects.get(chat_id=chat_id)
    message = chat.messages.last()
    message.sql_response = sql_response
    message.save()
    return message


def update_chat_answer(chat_id: str, answer: str) -> ChatMessage:
    chat = Chat.objects.get(chat_id=chat_id)
    message = chat.messages.last()
    message.answer = answer
    chat.save()
    message.save()
    return message


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
    chats =  Chat.objects.filter(google_user__google_id=user_id).values(
            "title", "updated_at", "chat_id"
        ).order_by('-updated_at')
    paginator = Paginator(chats, per_page)

    page_obj = paginator.get_page(page)
    chat_data = [
        {
            "chat_id": chat.chat_id,
            "title": chat.title,
            "created_at": chat.created_at,
            "updated_at": chat.updated_at,
            "chat_summary": chat.chat_summary,
        }
        for chat in page_obj.object_list
    ]

    return {
        "results": chat_data,
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
            "chat_summary": chat.chat_summary,
            "collection": chat.collection,
            "messages": [
                {
                    "question": msg.question,
                    "answer": msg.answer,
                    "intent_classification": msg.intent_classification,
                    "sql_response": msg.sql_response,
                    "created_at": msg.created_at,
                }
                for msg in messages
            ]
        }

    except Chat.DoesNotExist:
        return {"error": "Chat not found"}
