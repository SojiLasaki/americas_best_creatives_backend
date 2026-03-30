from django.contrib import admin
from .models import DesignerAssignment, DesignSubmission, RevisionRequest, AvailabilityProfile


@admin.register(DesignerAssignment)
class DesignerAssignmentAdmin(admin.ModelAdmin):
    list_display = ('quote', 'designer', 'assigned_by', 'status', 'assigned_at')
    list_filter = ('status',)


@admin.register(DesignSubmission)
class DesignSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'submitted_at')


@admin.register(RevisionRequest)
class RevisionRequestAdmin(admin.ModelAdmin):
    list_display = ('quote', 'customer', 'status', 'created_at')
    list_filter = ('status',)


@admin.register(AvailabilityProfile)
class AvailabilityProfileAdmin(admin.ModelAdmin):
    list_display = ('designer', 'available', 'active_tasks_count')
    list_filter = ('available',)
