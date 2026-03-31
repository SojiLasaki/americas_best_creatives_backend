from rest_framework import serializers
from .models import ChatRoom, ChatMessage
from apps.users.serializers import UserSerializer


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ('id', 'room', 'sender', 'message', 'created_at', 'seen')
        read_only_fields = ('sender', 'created_at')


class ChatRoomSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ('id', 'quote', 'participants', 'messages', 'created_at')
