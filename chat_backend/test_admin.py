from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from .admin import ConversationAdmin
from .models import Conversation, User


class ConversationAdminTestCase(TestCase):
    """
    Tests for ConversationAdmin class.
    """
    def setUp(self):
        self.user1 = User.objects.create(
            email='test1@example.com',
            first_name='Test',
            last_name='User',
            password='testpass',
            is_active=True)
        self.user2 = User.objects.create(
            email='test2@example.com',
            first_name='Test2',
            last_name='User2',
            password='testpass',
            is_active=True)
        # pylint: disable=no-member
        self.conversation = Conversation.objects.create(
            name=f"conv{self.user1.pk}_{self.user2.pk}"
        )
        self.conversation.members.set([self.user1, self.user2])
        self.admin = ConversationAdmin(Conversation, AdminSite())

    def test_name_method(self):
        """
        Test that the name method returns the correct value.
        """
        self.assertEqual(self.admin.name(self.conversation),
                         f"{self.conversation.name} "
                         f"{self.conversation.members}")

    def test_id_method(self):
        """
        Check that the id method returns the expected value.
        """
        self.assertEqual(self.admin.id(self.conversation),
                         str(self.conversation.id))
