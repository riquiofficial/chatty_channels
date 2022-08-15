import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


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
        message = event['message']
        print("sending to sockets...")
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("got ", message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group,
            {
                'type': 'chat_message',
                'message': message
            }
        )
