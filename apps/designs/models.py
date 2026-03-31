import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class DesignerAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    quote = models.ForeignKey('quotes.Quote', on_delete=models.CASCADE, related_name='designer_assignments')
    designer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='design_assignments')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assignments_made')
    assigned_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f'Assignment: Quote #{self.quote.pk} -> {self.designer.email}'


class DesignSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey(DesignerAssignment, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='design_submissions/')
    comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Submission for Assignment #{self.assignment.pk}'


class RevisionRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'

    quote = models.ForeignKey('quotes.Quote', on_delete=models.CASCADE, related_name='revisions')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='revision_requests')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Revision for Quote #{self.quote.pk}'


class AvailabilityProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    designer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='availability')
    available = models.BooleanField(default=True)
    expertise = models.JSONField(default=list, blank=True)
    active_tasks_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Availability: {self.designer.email} (available={self.available})'
