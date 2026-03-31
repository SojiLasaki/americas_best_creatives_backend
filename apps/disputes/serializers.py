from rest_framework import serializers
from .models import Dispute
from apps.users.serializers import UserSerializer


class DisputeSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    handled_by = UserSerializer(read_only=True)

    class Meta:
        model = Dispute
        fields = ('id', 'quote', 'customer', 'reason', 'status', 'handled_by', 'created_at', 'updated_at')
        read_only_fields = ('customer', 'created_at', 'updated_at')
