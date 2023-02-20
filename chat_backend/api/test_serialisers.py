"""
Test serialisers.py for messenger/api
"""
from django.test import TestCase
from chat_backend.models import Message, Conversation
from home.serialisers import UserSerializer
from home.models import User
from .serialisers import ConversationSerializer, MessageSerializer


class ConversationSerializerTestCase(TestCase):
    """
    Test case for the ConversationSerializer.
    """
    def setUp(self):
        self.user1 = User.objects.create(
            email='testtest@example.com',
            first_name='Test',
            last_name='User',
            password='testpass',
            is_active=True)
        self.user2 = User.objects.create(
            email='testtest2@example.com',
            first_name='Test2',
            last_name='User2',
            password='testpass2',
            is_active=True)
        # pylint: disable=no-member
        self.conversation = Conversation.objects.create(
            name=f"conv{self.user1.pk}_{self.user2.pk}")
        self.conversation.members.set([self.user1, self.user2])
        self.serializer = ConversationSerializer(
            instance=self.conversation, context={"user": self.user1})
        self.conversation.user = self.user1

    def test_serializer_has_expected_fields(self):
        """
        Test that the serializer has the expected fields.
        """
        expected_fields = ['id', 'name', 'other_user', 'last_message', 'user']
        self.assertEqual(list(self.serializer.fields.keys()), expected_fields)

    def test_other_user_field_returns_expected_data(self):
        """
        Test that the other_user field of the serialized data
        returns the correct data for the second CustomUser.
        """
        other_user_data = self.serializer.data["other_user"]
        self.assertEqual(other_user_data["pk"], self.user2.pk)

    def test_last_message_field_returns_expected_data(self):
        """
        Test that the last_message field of the serialized data
        returns the correct data for the last message in the Conversation.
        """
        # pylint: disable=no-member
        message = Message.objects.create(
            conversation=self.conversation,
            from_user=self.user1, to_user=self.user2,
            text="test message"
        )
        last_message_data = self.serializer.data["last_message"]
        self.assertEqual(last_message_data["text"], message.text)


class MessageSerializerTestCase(TestCase):
    """
    Test case for the MessageSerialiser class.
    """
    def setUp(self):
        self.user1 = User.objects.create(
            email='testtest@example.com',
            first_name='Test',
            last_name='User',
            password='testpass',
            is_active=True)
        self.user2 = User.objects.create(
            email='testtest2@example.com',
            first_name='Test2',
            last_name='User2',
            password='testpass2',
            is_active=True)
        # pylint: disable=no-member
        self.conversation = Conversation.objects.create(
            name=f"conv{self.user1.pk}_{self.user2.pk}")
        self.conversation.members.set([self.user1, self.user2])
        # pylint: disable=no-member
        self.message = Message.objects.create(
            conversation=self.conversation,
            from_user=self.user1, to_user=self.user2,
            text="test message"
        )
        self.serializer = MessageSerializer(
            instance=self.message)

    def test_serializer_has_expected_fields(self):
        """
        Test that the MessageSerializer has the expected fields.
        """
        expected_fields = [
            "id",
            "conversation",
            "from_user",
            "to_user",
            "text",
            "timestamp",
            "read",
        ]
        self.assertEqual(list(self.serializer.fields.keys()), expected_fields)

    def test_get_conversation_returns_expected_value(self):
        """
        Test that the get_conversation method returns the expected value.
        """
        self.assertEqual(self.serializer.get_conversation(
            self.message), str(self.conversation.pk))

    def test_get_from_user_returns_expected_data(self):
        """
        Test that the get_from_user method returns the expected data.
        """
        from_user_data = self.serializer.data['from_user']
        self.assertEqual(from_user_data, UserSerializer(
            self.message.from_user).data)

    def test_get_to_user_returns_expected_data(self):
        """
        Test that the get_to_user method returns the expected data.
        """
        to_user_data = self.serializer.data['to_user']
        self.assertEqual(to_user_data, UserSerializer(
            self.message.to_user).data)
