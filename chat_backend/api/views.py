from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
from django.db.models import Q
from django.db.utils import DatabaseError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from home.models import User
from chat_backend.api.pagynaters import MessagePagination
from chat_backend.api.serialisers import ConversationSerializer, MessageSerializer
from chat_backend.models import Conversation, Message


class ConversationViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    A viewset for viewing and retrieving Conversation objects.
    """
    serializer_class = ConversationSerializer
    # pylint: disable=no-member
    queryset = Conversation.objects.none()
    lookup_field = "name"

    def get_queryset(self):
        try:
            # pylint: disable=no-member
            queryset = Conversation.objects.filter(
                name__contains=self.request.user.pk
            )
            return queryset
        except DatabaseError as error:
            print(f'Error connecting to the database: {error}')
            return None

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return Response({"error": "Error connecting to the database"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}


class MessageViewSet(ListModelMixin, GenericViewSet):
    serializer_class = MessageSerializer
    # pylint: disable=no-member
    queryset = Message.objects.none()
    pagination_class = MessagePagination

    def get_queryset(self):
        """
        Return a queryset of conversations that contain the current
        user's ID in their name.
        """
        try:
            conversation_name = self.request.GET.get("conversation")
            queryset = (
                # pylint: disable=no-member
                Message.objects.filter(
                    Q(to_user=self.request.user.pk) |
                    Q(from_user=self.request.user.pk)
                )
                .filter(conversation__name=conversation_name)
                .order_by("-timestamp")
            )
            return queryset
        except DatabaseError as error:
            print(f'Error connecting to the database: {error}')
            return None

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return Response({"error": "Error connecting to the database"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
