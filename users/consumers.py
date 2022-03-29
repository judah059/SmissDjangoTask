import json

from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage, ChatRoom, CustomUser


class ChatConsumer(AsyncWebsocketConsumer):

    async def fetch_message(self, data):
        messages = sync_to_async(ChatMessage.objects.filter)(chat__room_name=data['room'])
        content = {
            'messages': self.messages_to_json(messages)
        }
        await self.send_chat_message(content)

    async def new_message(self, data):
        author = self.scope['user']
        room = self.scope['url_route']['kwargs']['room_name']
        author_user = sync_to_async(CustomUser.objects.filter)(username=author.username)
        current_room = sync_to_async(ChatRoom.objects.filter)(room_name=room)
        message = ChatMessage(
            content=data['message'],
            author=author_user,
            chat=current_room
        )
        print('!!! ', message.content, ' !!!')
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        sync_to_async(message.save)()
        await self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'result': {
                'chat': message.chat
            }
        }

    commands = {
        'fetch_message': fetch_message,
        'new_message': new_message
    }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)

    async def send_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps(message))
