from django.urls import path
from .views import DesignerTaskListView, DesignSubmissionCreateView, RevisionRequestCreateView

urlpatterns = [
    path('designer/tasks/', DesignerTaskListView.as_view(), name='designer-tasks'),
    path('designs/submit/', DesignSubmissionCreateView.as_view(), name='design-submit'),
    path('revisions/', RevisionRequestCreateView.as_view(), name='revision-create'),
]
