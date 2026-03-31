from django.urls import path
from .views import SupportTicketCreateView, SupportTicketListView

urlpatterns = [
    path('support/', SupportTicketCreateView.as_view(), name='support-create'),
    path('support/list/', SupportTicketListView.as_view(), name='support-list'),
]
