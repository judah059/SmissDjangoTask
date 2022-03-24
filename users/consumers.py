import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage, ChatRoom, CustomUser


class ChatConsumer(AsyncWebsocketConsumer):

    async def fetch_message(self, data):
        messages = ChatMessage.objects.filter(chat__room_name=data['room'])
        content = {
            'messages': self.messages_to_json(messages)
        }
        await self.send_chat_message(content)

    async def new_message(self, data):
        author = data['from']
        room = data['room']
        author_user = CustomUser.objects.filter(username=author)[0]
        current_room = ChatRoom.objects.filter(room_name=room)
        message = ChatMessage.objects.create(
            content=data['message'],
            author=author_user,
            chat=current_room
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        await self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'chat': message.chat,
            'author': message.author,
            'content': message.content,
            'created_at': str(message.created_at)
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

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

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
