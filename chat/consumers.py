import json
# from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Thread, Message
from django.db.models import ObjectDoesNotExist



class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['username'] # getting room name from url

        self.user = self.scope['user'] # getting authenticated user object

        self.friend = await self.get_user(self.room_name) # getting friend object

        # print(self.user, self.room_name)
        # print(self.friend)
      
        self.room = await self.get_thread(self.user, self.friend) # getting thread object
        # print(self.room)

        
        self.room_group_name = 'chat_%s' % self.room.id # creating room name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.create_message(self.user, message)
        response = {
                'message': message,
                'username': self.user.username,
            }

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': response
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


    @database_sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)

    @database_sync_to_async
    def get_thread(self, user, friend):
        self.thread = Thread.objects.filter(members__in=[user,friend]).first()

        if not self.thread: 
            self.thread = Thread(created=True)
            self.thread.save()
            self.thread.members.add(user,friend)
            return self.thread
        else:
            return self.thread

    @database_sync_to_async
    def create_message(self, me, msg):
        return Message.objects.create(thread=self.thread, user=me, message=msg)        


