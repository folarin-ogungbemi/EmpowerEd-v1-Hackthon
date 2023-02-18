from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(JsonWebsocketConsumer):
    """
    This consumer is used handle chat messages between users.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None

    def connect(self):
        print("Connected!")
        self.room_name = "home"
        self.accept()
        # because group_add is asynchronous, it would not work
        # without being converted to a synchronous function
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name,
        )
        self.send_json(
            {
                "type": "welcome_message",
                "message": "Hey, silly sausage! You've successfully connected!",
            }
        )

    def disconnect(self, code):
        print("Disconnected!")
        return super().disconnect(code)

    def receive_json(self, content, **kwargs):
        message_type = content["type"]
        if message_type == "chat_message":
            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    "type": "chat_message_echo",
                    "name": content["name"],
                    "message": content["message"],
                },
            )
        return super().receive_json(content, **kwargs)
    
    def chat_message_echo(self, event):
        print(event)
        self.send_json(event)