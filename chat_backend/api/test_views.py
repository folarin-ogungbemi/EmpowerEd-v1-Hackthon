"""
Tests for views.py of messenger/api.
"""
from django.test import RequestFactory
from rest_framework.test import APITestCase
from chat_backend.models import Conversation, Message
from home.models import User
from .views import ConversationViewSet, MessageViewSet


class ConversationViewSetTestCase(APITestCase):
    """
    Test case for the ConversationViewSet class.
    """
    def setUp(self):
        self.view = ConversationViewSet()
        self.factory = RequestFactory()
        self.user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass',
            is_active=True)
        self.view.request = self.factory.get("/api/conversations/")
        self.view.request.user = self.user

    def test_get_queryset(self):
        """
        Test that the view's get_queryset method returns conversations
        that contain the user's ID in the name.
        """
        # pylint: disable=no-member
        Conversation.objects.create(name=f"conv{self.user.pk}_123")
        # pylint: disable=no-member
        Conversation.objects.create(name=f"conv456_{self.user.pk}")
        # pylint: disable=no-member
        Conversation.objects.create(name=f"conv{self.user.pk}_789")
        # pylint: disable=no-member
        Conversation.objects.create(name="abc_def")

        # Check that the queryset returned by the view only includes
        # the conversations with the user's ID
        self.assertEqual(self.view.get_queryset().count(), 3)

    def test_get_serializer_context(self):
        """
        Test that get_serializer_context returns a dictionary
        containing the request and user from the view's request attribute.
        """
        context = self.view.get_serializer_context()
        self.assertEqual(context['request'], self.view.request)
        self.assertEqual(context['user'], self.view.request.user)


class MessageViewSetTestCase(APITestCase):
    """
    Test case for the MessageViewSet view.
    """
    def setUp(self):
        self.view = MessageViewSet()
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
            name=f"conv{self.user1.pk}_{self.user2.pk}"
        )
        # pylint: disable=no-member
        self.message1 = Message.objects.create(
            conversation=self.conversation,
            from_user=self.user2,
            to_user=self.user1,
            text="Test message 1"
        )
        # pylint: disable=no-member
        self.message2 = Message.objects.create(
            conversation=self.conversation,
            from_user=self.user1,
            to_user=self.user2,
            text="Test message 2"
        )
        # pylint: disable=no-member
        self.message3 = Message.objects.create(
            conversation=self.conversation,
            from_user=self.user1,
            to_user=self.user2,
            text="Test message 3"
        )
        self.conversation.members.set([self.user1, self.user2])
        self.client.force_authenticate(self.user1)
        self.request = RequestFactory().get("api/messages/")
        self.request.user = self.user1
        self.request.GET = self.request.GET.copy()
        self.request.GET["conversation"] = self.conversation.name

    def test_get_queryset(self):
        """
        Tests that the get_queryset method correctly filters and
        orders the messages by the conversation specified in the
        request and the current user.
        """
        self.view.request = self.request
        queryset = self.view.get_queryset()

        self.assertIn(self.message1, queryset)
        self.assertEqual(self.conversation, queryset.first().conversation)
        self.assertEqual(self.message3, queryset.first())
