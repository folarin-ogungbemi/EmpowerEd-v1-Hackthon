"""
Tests for consumers of messenger app.
"""
import asyncio
from uuid import uuid4
from unittest.mock import patch
from django.test import TestCase, TransactionTestCase
from channels.layers import InMemoryChannelLayer
from channels.testing import WebsocketCommunicator
from chat_backend.api.serialisers import MessageSerializer
from home.serialisers import UserSerializer
from home.models import User
from .models import Conversation, Message

from .consumers import UUIDEncoder, ChatConsumer, NotificationConsumer


class UUIDEncoderTests(TestCase):
    """
    Tests the UUIDEncoder class
    """
    def test_default_with_valid_uuid(self):
        """
        Test the default method of the UUIDEncoder class
        with a valid UUID object.
        """
        test_uuid = uuid4()
        encoder = UUIDEncoder()
        result = encoder.default(test_uuid)

        assert result == test_uuid.hex


class ChatConsumerTestCase(TransactionTestCase):
    """
    Unit tests for ChatConsumer
    """
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass')
        self.client.force_login(user=self.user)
        self.user2 = User.objects.create(
            email='test2@example.com',
            first_name='Test2',
            last_name='User2',
            password='testpass2')
        # pylint: disable=no-member
        self.conversation = Conversation.objects.create(
            name=f"conv{self.user.pk}_{self.user2.pk}"
        )
        self.conversation.members.set([self.user, self.user2])
        # pylint: disable=no-member
        self.message1 = Message.objects.create(
            conversation=self.conversation,
            from_user=self.user,
            to_user=self.user2,
            text="Test message 1"
        )
        self.url_route = {"kwargs": {
            "q": f"conv{self.user.pk}_{self.user2.pk}"}}

    @patch('channels.layers.channel_layers')
    async def test_connect(self, mock_channel_layers):
        """
        Tests if the connection is successful and sends a JSON message
        with the last 50 messages from the ChatConsumer class.
        """
        mock_channel_layers.__getitem__.return_value = InMemoryChannelLayer()
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(), "/testws/")
        communicator.scope["user"] = self.user
        communicator.scope["url_route"] = self.url_route
        connected = await communicator.connect()
        self.assertTrue(connected)
        response = await communicator.receive_json_from()
        self.assertEqual(
            response,
            {'type': "last_50_messages",
             'messages': [MessageSerializer(self.message1).data],
             'to_user': UserSerializer(self.user2).data,
             'has_more': False}
            )
        await communicator.disconnect()

    @patch('channels.layers.channel_layers')
    async def test_receive_json(self, mock_channel_layers):
        """
        Tests if the mothod receives and processes JSON correctly.
        """
        mock_channel_layers.__getitem__.return_value = InMemoryChannelLayer()
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(), "/testws/")
        communicator.scope["user"] = self.user
        communicator.scope["url_route"] = self.url_route
        connected = await communicator.connect()
        self.assertTrue(connected)
        communicator2 = WebsocketCommunicator(
            ChatConsumer.as_asgi(), "/testws/"
        )
        communicator2.scope["user"] = self.user2
        communicator2.scope["url_route"] = self.url_route
        await communicator2.connect()

        await communicator.send_json_to(
            {
                "type": "chat_message",
                "message": "Test message 2",
            }
        )
        # Wait for the second communicator to receive the chat_message_echo
        while True:
            try:
                response = await asyncio.wait_for(
                    communicator2.receive_json_from(), timeout=10
                    )
            except asyncio.TimeoutError:
                break
            if response["type"] == "chat_message_echo":
                break

        self.assertEqual(response["type"], "chat_message_echo")
        self.assertEqual(response["user_id"], self.user.pk)
        self.assertEqual(response["message"]['text'], "Test message 2")
        await communicator.disconnect()
        await communicator2.disconnect()

    @patch('channels.layers.channel_layers')
    async def test_read_messages(self, mock_channel_layers):
        """
        Tests if the received message is of the correct type
        and has the expected message text.
        """
        mock_channel_layers.__getitem__.return_value = InMemoryChannelLayer()
        # Set up a communicator for the user
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(), "/testws/")
        communicator.scope["user"] = self.user
        communicator.scope["url_route"] = self.url_route
        await communicator.connect()
        # Set up a communicator for the notification group
        notification_group_name = str(self.user.pk) + "__notifications"
        communicator2 = WebsocketCommunicator(
            NotificationConsumer.as_asgi(), "/testws/")
        communicator2.scope["user"] = self.user
        communicator2.scope["url_route"] = {
            "kwargs": {"q": notification_group_name}}
        await communicator2.connect()
        # Send a read_messages message
        await communicator.send_json_to({"type": "read_messages"})
        # Wait for the unread_count message to be sent
        while True:
            response = await communicator2.receive_json_from()
            if response["type"] == "unread_count":
                break

        self.assertEqual(response["unread_count"], 0)
        self.assertEqual(response["type"], "unread_count")

        await communicator.disconnect()
        await communicator2.disconnect()

    def test_get_receiver(self):
        """
        Tests that the method correctly retrieves another member
        of the conversation.
        """
        chat_consumer = ChatConsumer()
        chat_consumer.conversation_name = f"conv{self.user.pk}_{self.user2.pk}"
        chat_consumer.user = self.user

        receiver = chat_consumer.get_receiver()
        self.assertEqual(receiver, self.user2)

    def test_encode_json(self):
        """
        Test that the encode_json method correctly encodes
        a dictionary as JSON.
        """
        content = {'key': 'value'}
        json_str = ChatConsumer.encode_json(content)
        self.assertEqual(json_str, '{"key": "value"}')

    def test_new_message_notification(self):
        """
        Test that the new_message_notification method sends
        the correct event to the client.
        """
        event = {'event_type': 'new_message'}
        with patch.object(ChatConsumer, 'send_json') as mock_send_json:
            my_class_instance = ChatConsumer()
            my_class_instance.new_message_notification(event)
            mock_send_json.assert_called_with(event)


class NotificationConsumerTests(TransactionTestCase):
    """
    Integration tests for NotificationConsumer.
    """
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass')
        self.client.force_login(user=self.user)
        self.user2 = User.objects.create(
            email='test2@example.com',
            first_name='Test2',
            last_name='User2',
            password='testpass2')
        # pylint: disable=no-member
        self.conversation = Conversation.objects.create(
            name=f"conv{self.user.pk}_{self.user2.pk}"
        )
        self.conversation.members.set([self.user, self.user2])
        # pylint: disable=no-member
        self.message1 = Message.objects.create(
            conversation=self.conversation,
            from_user=self.user,
            to_user=self.user2,
            text="Test message 1"
        )
        # pylint: disable=no-member
        self.message2 = Message.objects.create(
            conversation=self.conversation,
            from_user=self.user2,
            to_user=self.user,
            text="Test message 1"
        )

    @patch('channels.layers.channel_layers')
    async def test_connect(self, mock_channel_layers):
        """
        Tests if the connection is successful and sends a JSON message
        with the count of unread messages.
        """
        mock_channel_layers.__getitem__.return_value = InMemoryChannelLayer()
        communicator = WebsocketCommunicator(
            NotificationConsumer.as_asgi(), "/testws/")
        communicator.scope["user"] = self.user
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        unread_count = 1
        each = [[self.user2.pk, unread_count]]
        expected_message = {
            "type": "unread_count",
            "unread_count": unread_count,
            "each": each,
        }
        received_message = await communicator.receive_json_from()
        self.assertEqual(received_message, expected_message)

    def test_new_message_notification(self):
        """
        Test that the new_message_notification method sends
        the correct event to the client.
        """
        event = {'event_type': 'new_message'}
        with patch.object(ChatConsumer, 'send_json') as mock_send_json:
            consumer = ChatConsumer()
            consumer.new_message_notification(event)
            mock_send_json.assert_called_with(event)

    def test_unread_count_notification(self):
        """
        Test that the unread_count method sends
        the correct event to the client.
        """
        event = {'event_type': 'unread_count'}
        with patch.object(ChatConsumer, 'send_json') as mock_send_json:
            consumer = ChatConsumer()
            consumer.unread_count(event)
            mock_send_json.assert_called_with(event)

#######################################################

#   to run integration tests locally you need to run
#   Redis locally first:
#   instal: sudo apt-get install redis-server
#   run: redis-server --daemonize yes

#######################################################


# class ChatConsumerIntegrationTestCase(TransactionTestCase):
#     """
#     Integration tests for ChatConsumer.
#     """
#     def setUp(self):
#         # Set up a testing channel layer
#         self.channel_layer = self.create_channel_layer()
#         self.user = User.objects.create(
#             email='test@example.com',
#             first_name='Test',
#             last_name='User',
#             password='testpass')
#         self.client.force_login(user=self.user)
#         self.user2 = User.objects.create(
#             email='test2@example.com',
#             first_name='Test2',
#             last_name='User2',
#             password='testpass2')
#         # pylint: disable=no-member
#         self.conversation = Conversation.objects.create(
#             name=f"conv{self.user.pk}_{self.user2.pk}"
#         )
#         self.conversation.members.set([self.user, self.user2])
#         # pylint: disable=no-member
#         self.message1 = Message.objects.create(
#             conversation=self.conversation,
#             from_user=self.user,
#             to_user=self.user2,
#             text="Test message 1"
#         )
#         self.url_route = {"kwargs": {
#             "q": f"conv{self.user.pk}_{self.user2.pk}"}}

#     def create_channel_layer(self):
#         from channels.layers import get_channel_layer
#         return get_channel_layer()

#     async def test_connect(self):
#         communicator = WebsocketCommunicator(
#             ChatConsumer.as_asgi(), "/testws/")
#         communicator.scope["user"] = self.user
#         communicator.scope["url_route"] = self.url_route
#         connected = await communicator.connect()
#         self.assertTrue(connected)
#         response = await communicator.receive_json_from()
#         self.assertEqual(
#             response,
#             {'type': "last_50_messages",
#              'messages': [MessageSerializer(self.message1).data],
#              'to_user': UserSerializer(self.user2).data,
#              'has_more': False}
#              )
#         await communicator.disconnect()

#     async def test_receive_json(self):
#         communicator = WebsocketCommunicator(
#             ChatConsumer.as_asgi(), "/testws/")
#         communicator.scope["user"] = self.user
#         communicator.scope["url_route"] = self.url_route
#         connected = await communicator.connect()
#         self.assertTrue(connected)
#         # Connect the second communicator
#         communicator2 = WebsocketCommunicator(
#             ChatConsumer.as_asgi(), "/testws/"
#         )
#         communicator2.scope["user"] = self.user2
#         communicator2.scope["url_route"] = self.url_route
#         await communicator2.connect()

#         await communicator.send_json_to(
#             {
#                 "type": "chat_message",
#                 "message": "Test message 2",
#             }
#         )
#         # Wait for the second communicator to receive the chat_message_echo
#         while True:
#             try:
#                 response = await asyncio.wait_for(
#                     communicator2.receive_json_from(), timeout=10
#                     )
#             except asyncio.TimeoutError:
#                 break
#             if response["type"] == "chat_message_echo":
#                 break

#         self.assertEqual(response["type"], "chat_message_echo")
#         self.assertEqual(response["user_id"], self.user.pk)
#         self.assertEqual(response["message"]['text'], "Test message 2")

#         await communicator.disconnect()
#         await communicator2.disconnect()

#     async def test_read_messages(self):
#         # Set up a communicator for the user
#         communicator = WebsocketCommunicator(
#             ChatConsumer.as_asgi(), "/testws/")
#         communicator.scope["user"] = self.user
#         communicator.scope["url_route"] = self.url_route
#         await communicator.connect()

#         # Set up a communicator for the notification group
#         notification_group_name = str(self.user.pk) + "__notifications"
#         communicator2 = WebsocketCommunicator(
#             NotificationConsumer.as_asgi(), "/testws/")
#         communicator2.scope["user"] = self.user
#         communicator2.scope["url_route"] = {
#             "kwargs": {"q": notification_group_name}}
#         await communicator2.connect()

#         # Send a read_messages message
#         await communicator.send_json_to({"type": "read_messages"})

#         while True:
#             response = await communicator2.receive_json_from()
#             if response["type"] == "unread_count":
#                 break

#         self.assertEqual(response["unread_count"], 0)
#         self.assertEqual(response["type"], "unread_count")

#         await communicator.disconnect()
#         await communicator2.disconnect()
    

# class NotificationConsumerIntegrationTests(TransactionTestCase):
#     """
#     Integration tests for NotificationConsumer.
#     """
#     def setUp(self):
#         self.channel_layer = self.create_channel_layer()
#         self.user = User.objects.create(
#             email='test@example.com',
#             first_name='Test',
#             last_name='User',
#             password='testpass')
#         self.client.force_login(user=self.user)
#         self.user2 = User.objects.create(
#             email='test2@example.com',
#             first_name='Test2',
#             last_name='User2',
#             password='testpass2')
#         # pylint: disable=no-member
#         self.conversation = Conversation.objects.create(
#             name=f"conv{self.user.pk}_{self.user2.pk}"
#         )
#         self.conversation.members.set([self.user, self.user2])
#         # pylint: disable=no-member
#         self.message1 = Message.objects.create(
#             conversation=self.conversation,
#             from_user=self.user,
#             to_user=self.user2,
#             text="Test message 1"
#         )
#         # pylint: disable=no-member
#         self.message2 = Message.objects.create(
#             conversation=self.conversation,
#             from_user=self.user2,
#             to_user=self.user,
#             text="Test message 1"
#         )

#     def create_channel_layer(self):
#         from channels.layers import get_channel_layer
#         return get_channel_layer()

#     async def test_connect(self):
#         communicator = WebsocketCommunicator(
#             NotificationConsumer.as_asgi(), "/testws/"
#         )
#         communicator.scope["user"] = self.user
#         connected = await communicator.connect()
#         self.assertTrue(connected)
#         self.assertTrue(self.user.is_authenticated)

#         response = await communicator.receive_json_from()
#         self.assertEqual(response["type"], "unread_count")
#         self.assertEqual(response["unread_count"], 1)
#         self.assertEqual(response["each"], [[self.user2.pk, 1]])

#         await communicator.disconnect()

