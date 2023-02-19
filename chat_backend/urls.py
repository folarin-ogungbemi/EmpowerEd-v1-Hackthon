from django.urls import path
from .views import MessagesView


app_name = 'chat_backend'


urlpatterns = [
    path('', MessagesView.as_view(), name='conv_list'),
    path('chat/<path:path>', MessagesView.as_view(), name='messages_with_path')
]
