from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from uuid import UUID
from chat_backend.api.serialisers import MessageSerializer
from home.serialisers import UserSerializer
from .models import Conversation, Message
from home.models import User


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class ChatConsumer(JsonWebsocketConsumer):
    """
    This consumer is used handle chat messages between users.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.conversation_name = None
        self.conversation = None

    def connect(self):
        self.user = self.scope['user']

        self.accept()
        self.conversation_name = f"{self.scope['url_route']['kwargs']['q']}"
        self.conversation, created = Conversation.objects.get_or_create(
            name=self.conversation_name
            )

        # because group_add is asynchronous, it would not work
        # without being converted to a synchronous function
        async_to_sync(self.channel_layer.group_add)(
            self.conversation_name,
            self.channel_name,
        )

        messages = self.conversation.messages.all().order_by("-timestamp")[0:10]
        user = self.get_receiver()
        message_count = self.conversation.messages.all().count()
        self.send_json(
            {
                "type": "last_50_messages",
                "messages": MessageSerializer(messages, many=True).data,
                "to_user": UserSerializer(user).data,
                "has_more": message_count > 10,
            }
        )

    def disconnect(self, code):
        print("Disconnected!")
        return super().disconnect(code)

    def get_receiver(self):
        ids = self.conversation_name[4:].split("_")
        for user_id in ids:
            if int(user_id) != self.user.pk:
                return User.objects.get(pk=user_id)

    def receive_json(self, content, **kwargs):
        message_type = content["type"]
        if message_type == "chat_message":
            message = Message.objects.create(
                from_user=self.user,
                to_user=self.get_receiver(),
                text=content["message"],
                conversation=self.conversation,
            )

            async_to_sync(self.channel_layer.group_send)(
                self.conversation_name,
                {
                    "type": "chat_message_echo",
                    "name": self.user.pk,
                    "message": MessageSerializer(message).data,
                },
            )

        return super().receive_json(content, **kwargs)
    
    def chat_message_echo(self, event):
        print(event)
        self.send_json(event)

    @classmethod
    def encode_json(cls, content):
        return json.dumps(content, cls=UUIDEncoder)
