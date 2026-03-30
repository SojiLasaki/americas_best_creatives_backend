from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Quote, QuoteDocument
from .serializers import (
    QuoteSerializer, QuoteCreateSerializer, QuoteStatusSerializer, QuoteDocumentSerializer
)
from apps.permissions import (
    IsAdminOrSuperAdmin, IsAgentOrAdmin, IsCustomer, IsOwnerOrAdmin
)
from apps.services import QuoteService, QuoteApprovalService, DesignerAssignmentService


class QuoteViewSet(ModelViewSet):
    serializer_class = QuoteSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin:
            return Quote.objects.all().select_related('customer', 'catalog', 'station')
        if user.is_admin:
            try:
                station = user.profile.station
                return Quote.objects.filter(station=station).select_related('customer', 'catalog', 'station')
            except Exception:
                return Quote.objects.none()
        if user.is_agent:
            try:
                station = user.profile.station
                return Quote.objects.filter(station=station).select_related('customer', 'catalog', 'station')
            except Exception:
                return Quote.objects.none()
        return Quote.objects.filter(customer=user).select_related('customer', 'catalog', 'station')

    def get_serializer_class(self):
        if self.action == 'create':
            return QuoteCreateSerializer
        if self.action == 'partial_update':
            return QuoteStatusSerializer
        return QuoteSerializer

    def perform_create(self, serializer):
        user = self.request.user
        agent = user if user.is_agent else None
        quote = serializer.save(customer=user, created_by_agent=agent)
        return quote

    @action(detail=True, methods=['post'], url_path='upload-quote',
            parser_classes=[MultiPartParser, FormParser])
    def upload_quote(self, request, pk=None):
        quote = self.get_object()
        serializer = QuoteDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(quote=quote, uploaded_by=request.user)
            quote.status = Quote.Status.QUOTED
            quote.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        quote = self.get_object()
        result = QuoteApprovalService.approve(quote, request.user)
        return Response({'status': quote.status, 'detail': result})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        quote = self.get_object()
        result = QuoteApprovalService.reject(quote, request.user)
        return Response({'status': quote.status, 'detail': result})

    @action(detail=True, methods=['post'], url_path='assign-designer')
    def assign_designer(self, request, pk=None):
        quote = self.get_object()
        designer_id = request.data.get('designer_id')
        assignment = DesignerAssignmentService.assign(quote, request.user, designer_id)
        from apps.designs.serializers import DesignerAssignmentSerializer
        return Response(DesignerAssignmentSerializer(assignment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        quote = self.get_object()
        serializer = QuoteStatusSerializer(quote, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
