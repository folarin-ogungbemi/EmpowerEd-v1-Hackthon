from django.urls import path

from chat_backend.consumers import ChatConsumer, NotificationConsumer

websocket_urlpatterns = [
    path("messages/chat/<q>", ChatConsumer.as_asgi()),
    path("notifications/", NotificationConsumer.as_asgi())]