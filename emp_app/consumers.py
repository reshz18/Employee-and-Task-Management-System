import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from .models import ChatRoom, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Debugging: Print connection status
        print(f"WebSocket Connected: Room - {self.room_name}")

        # Join the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Debugging: Print disconnect status
        print(f"WebSocket Disconnected: Room - {self.room_name}")
        
        # Leave the room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        username = data.get("username")
        room_name = data.get("room_name")

        # Debugging: Print received data
        print(f"Received message: {message} from {username} in {room_name}")

        user = await User.objects.aget(email_address=username)  # Using email instead of username
        
        # Ensure the chat room exists
        chat_room, created = await ChatRoom.objects.aget_or_create(name=room_name)
        if created:
            print(f"Chat Room '{room_name}' created successfully.")
        
        # Save message to database
        await Message.objects.acreate(chat_room=chat_room, sender=user, content=message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Debugging: Print message broadcast status
        print(f"Broadcasting message: {message} from {username}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "username": username}))