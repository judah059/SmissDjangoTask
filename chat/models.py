from django.db import models
from users.models import CustomUser


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=120)
    first_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='first')
    second_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='second')
    created_at = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):
    content = models.TextField(default=None)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)