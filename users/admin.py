from dataclasses import field
from django.contrib import admin
from .models import CustomUser, ChatRoom, ChatMessage


admin.site.register(CustomUser)
admin.site.register(ChatRoom)
admin.site.register(ChatMessage)

