import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

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
        user = data['user']
        message = data['message']

        await self.save_message(self.room_name, user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'user':user,
                'message':message
            }
        )
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message':event['message'],
            'user':event['user']
        }))
    
    @sync_to_async
    def save_message(self, room, user, message):
        Message.objects.create(room_name=room,user=user,content=message)