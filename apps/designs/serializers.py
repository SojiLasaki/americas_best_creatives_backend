from rest_framework import serializers
from .models import DesignerAssignment, DesignSubmission, RevisionRequest, AvailabilityProfile
from apps.users.serializers import UserSerializer


class DesignerAssignmentSerializer(serializers.ModelSerializer):
    designer = UserSerializer(read_only=True)
    assigned_by = UserSerializer(read_only=True)

    class Meta:
        model = DesignerAssignment
        fields = ('id', 'quote', 'designer', 'assigned_by', 'assigned_at', 'status')
        read_only_fields = ('designer', 'assigned_by', 'assigned_at')


class DesignSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignSubmission
        fields = ('id', 'assignment', 'file', 'comment', 'submitted_at')
        read_only_fields = ('submitted_at',)


class RevisionRequestSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)

    class Meta:
        model = RevisionRequest
        fields = ('id', 'quote', 'customer', 'message', 'status', 'created_at')
        read_only_fields = ('customer', 'created_at')


class AvailabilityProfileSerializer(serializers.ModelSerializer):
    designer = UserSerializer(read_only=True)

    class Meta:
        model = AvailabilityProfile
        fields = ('id', 'designer', 'available', 'expertise', 'active_tasks_count')
