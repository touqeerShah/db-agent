from django.urls import path
from .views import (
    get_user_details,
    create_user,
    verify_google_token,
    ReportGenerationView,
    ChatMessagesView,
    ListChatView,
    ChatDeleteView
)

urlpatterns = [
    path("list_chat/", ListChatView.as_view(), name="list_chat"),  # List all user chats
    path(
        "chat_details/<str:chat_id>/", ChatMessagesView.as_view(), name="chat_details"
    ),  # Details for a specific chat
    path("chat_delete/<str:chat_id>/", ChatDeleteView.as_view(), name="chat_delete"),
    path(
        "report_stream/<str:chat_id>/",
        ReportGenerationView.as_view(),
        name="report_stream",
    ),  # Stream report for a chat
    path(
        "get_user/<str:google_id>", get_user_details, name="get_user"
    ),  # Get user details
    path("create_user/", create_user, name="create_user"),  # Create a new user
    path(
        "verify_google_token/", verify_google_token, name="verify_google_token"
    ),  # Verify Google token
]
