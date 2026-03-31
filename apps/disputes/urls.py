from django.urls import path
from .views import DisputeCreateView, DisputeListView

urlpatterns = [
    path('disputes/', DisputeCreateView.as_view(), name='dispute-create'),
    path('disputes/list/', DisputeListView.as_view(), name='dispute-list'),
]
