import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message,Profile
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name = f'user_{self.user.username}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender_username = self.scope['user'].username
        receiver_username = data['receiver']
        content = data['message']

        await self.save_message(sender_username, receiver_username, content)

        await self.channel_layer.group_send(
            f'user_{receiver_username}',
            {
                'type':'chat_message',
                'sender':sender_username,
                'receiver ':receiver_username,
                'message': content
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "sender": event["sender"],
            "receiver": event["receiver"],
            "message": event["message"],
        }))
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
    
    @sync_to_async
    def save_message(self, sender_username, receiver_username, message):
        try:
            sender_profile = Profile.objects.get(user__username=sender_username)
            receiver_profile = Profile.objects.get(user__username=receiver_username)
        except Profile.DoesNotExist:
            sender_user = User.objects.get(username=sender_username)
            sender_profile = Profile.objects.create(user=sender_user)
            receiver_user = User.objects.get(username=receiver_username)
            receiver_profile = Profile.objects.create(user=receiver_user)

        room_name = f"{min(sender_username, receiver_username)}__{max(sender_username, receiver_username)}"
        Message.objects.create(
            room_name=room_name,
            sender=sender_profile,
            receiver=receiver_profile,
            content=message
        )


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f'group_{self.room_name}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender_username = data['sender']
        content = data['message']

        await self.save_message(self.room_name, sender_username, content)

        await self.channel_layer.group_send(
            self.group_name,{
                "type":"group_message",
                "room_name":self.room_name,
                "sender":sender_username,
                "message":content
            }
        )

    async def group_message(self, event):
        await self.send(text_data=json.dumps({
            "room_name": event["room_name"],
            "sender": event["sender"],
            "message": event["message"],
        }))

    @sync_to_async
    def save_message(self, room_name, sender_username, content):
        sender = Profile.objects.get(user__username=sender_username)
        Message.objects.create(
            room_name=room_name,
            sender=sender,
            receiver=None,
            content=content
        )