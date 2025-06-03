from django.db import models


class GoogleUser(models.Model):
    google_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    picture = models.URLField(max_length=500)
    role = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Chat(models.Model):
    chat_id = models.CharField(max_length=255, unique=True)
    google_user = models.ForeignKey("GoogleUser", on_delete=models.CASCADE)
    collection = models.JSONField(default=list, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chat_summary = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)  # Collection name if a file is uploaded
    # New: related ChatMessages
    def __str__(self):
        return f"Chat {self.chat_id} for {self.google_user.name}"


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)

    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Store response data and classification
    intent_classification = models.JSONField(
        blank=True, null=True
    )  # e.g., {"intent": "search_db", "reason": "..."}
    sql_response = models.JSONField(
        blank=True, null=True
    )  # e.g., {"is_allow": true, "query": [...]}

    def __str__(self):
        return f"Message in Chat {self.chat.chat_id}"
