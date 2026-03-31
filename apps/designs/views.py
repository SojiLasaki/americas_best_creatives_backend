from rest_framework import generics, permissions, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import DesignerAssignment, DesignSubmission, RevisionRequest
from .serializers import (
    DesignerAssignmentSerializer, DesignSubmissionSerializer, RevisionRequestSerializer
)
from apps.permissions import IsDesigner, IsCustomer


class DesignerTaskListView(generics.ListAPIView):
    serializer_class = DesignerAssignmentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return DesignerAssignment.objects.filter(
            designer=self.request.user
        ).select_related('quote', 'assigned_by')


class DesignSubmissionCreateView(generics.CreateAPIView):
    serializer_class = DesignSubmissionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        assignment = serializer.validated_data['assignment']
        serializer.save()
        assignment.status = DesignerAssignment.Status.IN_PROGRESS
        assignment.save()


class RevisionRequestCreateView(generics.CreateAPIView):
    serializer_class = RevisionRequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
