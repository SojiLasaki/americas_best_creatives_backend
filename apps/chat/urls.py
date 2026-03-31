from django.urls import path
from .views import ChatRoomView, ChatMessageSendView

urlpatterns = [
    path('chat/<uuid:quote_id>/', ChatRoomView.as_view(), name='chat-room'),
    path('chat/send/', ChatMessageSendView.as_view(), name='chat-send'),
]
