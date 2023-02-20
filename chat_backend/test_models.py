"""
Tests for models of messenger app.
"""
import uuid
from django.db.models import (UUIDField, ForeignKey, CharField,
                              BooleanField, DateTimeField, ManyToManyField)
from django.test import TestCase
from home.models import User
from .models import Conversation, Message


class ConversationTestCase(TestCase):
    """
    Tests for Conversation model class.
    """
    def setUp(self):
        # pylint: disable=no-member
        self.user1 = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass',
            is_active=True)
        # pylint: disable=no-member
        self.user2 = User.objects.create(
            email='test@example2.com',
            first_name='Test2',
            last_name='User2',
            password='testpass2',
            is_active=True)
        # pylint: disable=no-member
        self.conversation = Conversation.objects.create(
            name=f"conv{self.user1.pk}_{self.user2.pk}")
        self.conversation.members.set([self.user1, self.user2])

    def test_id_field(self):
        """
        Test the 'id' field of the Conversation model.
        """
        # pylint: disable=no-member
        field = Conversation._meta.get_field("id")
        self.assertEqual(field.__class__.__name__, "UUIDField")
        self.assertEqual(field.default, uuid.uuid4)
        self.assertFalse(field.editable)

    def test_name_field(self):
        """
        Test the 'name' field of the Conversation model.
        """
        # pylint: disable=no-member
        field = Conversation._meta.get_field("name")
        self.assertEqual(field.__class__.__name__, "CharField")
        self.assertEqual(field.max_length, 128)

    def test_members_field(self):
        """
        Test that the members field is a ManyToManyField
        with the correct related model.
        """
        field = self.conversation._meta.get_field("members")
        self.assertIsInstance(field, ManyToManyField)
        self.assertEqual(field.related_model, User)

    def test_str_representation(self):
        """
        Test string representation of the Conversation model.
        """
        self.assertEqual(str(self.conversation), self.conversation.name)


class MessageModelTests(TestCase):
    """
    Tests for Message model class.
    """
    def setUp(self):
        # pylint: disable=no-member
        self.user1 = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass',
            is_active=True)
        # pylint: disable=no-member
        self.user2 = User.objects.create(
            email='test@example2.com',
            first_name='Test2',
            last_name='User2',
            password='testpass2',
            is_active=True)
        # pylint: disable=no-member
        self.conversation = Conversation.objects.create(
            name=f"conv{self.user1.pk}_{self.user2.pk}")
        self.conversation.members.set([self.user1, self.user2])
        # pylint: disable=no-member
        self.message1 = Message.objects.create(
            conversation=self.conversation,
            from_user=self.user2,
            to_user=self.user1,
            text="Test message 1"
        )

    def test_id_field(self):
        """
        Test the 'id' field of the Message model.
        """
        # pylint: disable=no-member
        field = Message._meta.get_field("id")
        self.assertIsInstance(field, UUIDField)
        self.assertTrue(field.primary_key)
        self.assertEqual(field.default, uuid.uuid4)
        self.assertFalse(field.editable)

    def test_conversation_field(self):
        """
        Test the 'conversation' field of the Message model.
        """
        # pylint: disable=no-member
        field = Message._meta.get_field("conversation")
        self.assertIsInstance(field, ForeignKey)
        self.assertEqual(field.related_model, Conversation)

    def test_from_user_field(self):
        """
        Test the 'from_user' field of the Message model.
        """
        # pylint: disable=no-member
        field = Message._meta.get_field("from_user")
        self.assertIsInstance(field, ForeignKey)
        self.assertEqual(field.related_model, User)

    def test_to_user_field(self):
        """
        Test the 'to_user' field of the Message model.
        """
        self.assertEqual(self.message1.to_user, self.user1)

    def test_text_field(self):
        """
        Test the 'text' field of the Message model.
        """
        # pylint: disable=no-member
        field = Message._meta.get_field("text")
        self.assertIsInstance(field, CharField)
        self.assertEqual(field.max_length, 512)

    def test_timestamp_field(self):
        """
        Test the 'timestamp' field of the Message model.
        """
        # pylint: disable=no-member
        field = Message._meta.get_field('timestamp')
        self.assertIsInstance(field, DateTimeField)
        self.assertTrue(field.auto_now_add)

    def test_read_field(self):
        """
        Test the 'read' field of the Message model.
        """
        # pylint: disable=no-member
        field = Message._meta.get_field("read")
        self.assertIsInstance(field, BooleanField)

    def test_str_representation(self):
        """
        Test string representation of the Message model.
        """
        self.assertEqual(str(self.conversation), self.conversation.name)

