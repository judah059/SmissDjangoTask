import datetime
import json

from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage, ChatRoom, CustomUser


class ChatConsumer(AsyncWebsocketConsumer):


    async def new_message(self, data):
        author = self.scope['user']
        room = self.scope['url_route']['kwargs']['room_name']
        author_user = await sync_to_async(CustomUser.objects.get)(username=author.username)
        current_room = await sync_to_async(ChatRoom.objects.get)(room_name=room)
        print('aaaaaaaaaaa')
        message = await sync_to_async(ChatMessage)(content=data['message'], author=author_user, chat=current_room)
        print('hellooo')
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        print('im here!!!!!!!')
        await sync_to_async(message.save)()
        print('hiiiii', datetime.datetime.now())
        await self.send_chat_message(content)
        print('the end)')

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'content': message.content,
            'author': message.author.username,
            'chat': message.chat.room_name,
            'created_at': str(message.created_at)
        }

    commands = {
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
        print(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps(message))
