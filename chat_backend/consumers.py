"""
Consumers of the Messenger app.
"""
import json
from uuid import UUID
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from chat_backend.api.serialisers import MessageSerializer
from home.serialisers import UserSerializer
from home.models import User
from .models import Conversation, Message


class UUIDEncoder(json.JSONEncoder):
    """
    A custom JSON encoder for UUID objects.
    """

    def default(self, o):
        """
        Encodes a UUID object as a hexadecimal string.
        """
        if isinstance(o, UUID):
            # if the object is uuid, it returns the value of uuid
            return o.hex
        return json.JSONEncoder.default(self, o)


class ChatConsumer(JsonWebsocketConsumer):
    """
    This consumer is used handle chat messages between users.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.conversation_name = None
        self.conversation = None

    # pylint: disable=unused-argument
    def connect(self, *args):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            return

        self.accept()
        self.conversation_name = f"{self.scope['url_route']['kwargs']['q']}"
        split_name = (list(map(int, self.conversation_name[4:].split("_"))))
        split_name.sort()
        # pylint: disable=no-member, unused-variable
        self.conversation, created = Conversation.objects.get_or_create(
            name=f"conv{split_name[0]}_{split_name[1]}"
        )
        for user_id in split_name:
            self.conversation.members.add(User.objects.get(pk=user_id))

        # because group_add is asynchronous, it would not work
        # without being converted to a synchronous function
        async_to_sync(self.channel_layer.group_add)(
            self.conversation_name,
            self.channel_name,
        )

        # sends a message containing the last 50 messages in the conversation
        messages = self.conversation.messages.all().order_by(
            "-timestamp")[0:50]
        user = self.get_receiver()
        message_count = self.conversation.messages.all().count()
        if self.user in self.conversation.members.all():
            self.send_json(
                {
                    "type": "last_50_messages",
                    "messages": MessageSerializer(messages, many=True).data,
                    "to_user": UserSerializer(user).data,
                    "has_more": message_count > 50,
                }
            )

    def disconnect(self, code):
        print("Disconnected!")
        return super().disconnect(code)

    def get_receiver(self):
        """
        Retrieves another member of the conversation.
        """
        ids = self.conversation_name[4:].split("_")
        for user_id in ids:
            if int(user_id) != self.user.pk:
                return User.objects.get(pk=user_id)

    def receive_json(self, content, **kwargs):
        message_type = content["type"]
        if message_type == "chat_message":
            # creates a new message
            # pylint: disable=no-member
            message = Message.objects.create(
                from_user=self.user,
                to_user=self.get_receiver(),
                text=content["message"],
                conversation=self.conversation,
            )
            # sends it to the other user in the conversation
            async_to_sync(self.channel_layer.group_send)(
                self.conversation_name,
                {
                    "type": "chat_message_echo",
                    "user_id": self.user.pk,
                    "message": MessageSerializer(message).data,
                },
            )
            # sends a notification to the other user
            notification_group_name = str(
                self.get_receiver().pk) + "__notifications"
            async_to_sync(self.channel_layer.group_send)(
                notification_group_name,
                {
                    "type": "new_message_notification",
                    "name": self.user.pk,
                    "message": MessageSerializer(message).data,
                },
            )

        if message_type == "read_messages":
            # marks messages sent to the user as read
            messages_to_me = self.conversation.messages.filter(
                to_user=self.user)
            messages_to_me.update(read=True)

            # Update the unread message count
            # pylint: disable=no-member
            unread_count = Message.objects.filter(
                to_user=self.user, read=False).count()
            async_to_sync(self.channel_layer.group_send)(
                str(self.user.pk) + "__notifications",
                {
                    "type": "unread_count",
                    "unread_count": unread_count,
                },
            )

        return super().receive_json(content, **kwargs)

    def chat_message_echo(self, event):
        """
        Sends a chat message event to the client through
        the WebSocket connection.
        """
        self.send_json(event)

    @classmethod
    def encode_json(cls, content):
        return json.dumps(content, cls=UUIDEncoder)

    def new_message_notification(self, event):
        """
        Sends a new message notification event to the client
        through the WebSocket connection.
        """
        self.send_json(event)

    def unread_count(self, event):
        """
        Sends an unread message count event to the client
        through the WebSocket connection.
        """
        self.send_json(event)


class NotificationConsumer(JsonWebsocketConsumer):
    """
    This consumer is used to send notifications.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.notification_group_name = None
        self.user = None

    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            return

        self.accept()
        # private notification group
        self.notification_group_name = str(self.user.pk) + "__notifications"
        async_to_sync(self.channel_layer.group_add)(
            self.notification_group_name,
            self.channel_name,
        )

        # count of unread messages
        # pylint: disable=no-member
        have_notifications = Message.objects.filter(
            to_user=self.user, read=False)
        unread_count = have_notifications.count()
        from_user = [item.from_user.pk for item in have_notifications]
        each = list(
            {(fr_user, have_notifications.filter(from_user=fr_user).count())
             for fr_user in from_user}
        )
        self.send_json(
            {
                "type": "unread_count",
                "unread_count": unread_count,
                "each": each,
            }
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.notification_group_name,
            self.channel_name,
        )
        return super().disconnect(code)

    def new_message_notification(self, event):
        """
        Sends a new message notification event to the client
        through the WebSocket connection.
        """
        self.send_json(event)

    def unread_count(self, event):
        """
        Sends an unread message count event to the client
        through the WebSocket connection.
        """
        self.send_json(event)
