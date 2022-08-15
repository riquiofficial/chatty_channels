import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatRoom, Message

from django.contrib.auth import get_user_model
User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room = self.scope['url_route']['kwargs']['room']
        self.group = 'chat_%s' % self.room

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group,
            self.channel_name
        )

    # Receive message from room group
    def chat_message(self, event):
        new_message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # save to the db
        user = User.objects.get(pk=text_data_json['user'])
        room = ChatRoom.objects.get(pk=self.room)
        new_message = Message.objects.create(sender=user,
                                             room=room, body=message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group,
            {
                'type': 'chat_message',
                'message': new_message.body,
                'user': new_message.sender.username,
                'timestamp': new_message.timestamp.__str__(),
            }
        )
