from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer


class ChatRoomView(generics.RetrieveAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        quote_id = self.kwargs['quote_id']
        room, _ = ChatRoom.objects.get_or_create(quote_id=quote_id)
        room.participants.add(self.request.user)
        return room


class ChatMessageSendView(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
