from django.urls import path

from chat_backend.consumers import ChatConsumer

websocket_urlpatterns = [path("messages/chat/<q>", ChatConsumer.as_asgi())]
