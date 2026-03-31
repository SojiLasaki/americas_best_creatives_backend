from django.contrib import admin
from .models import Dispute


@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ('id', 'quote', 'customer', 'status', 'handled_by', 'created_at')
    list_filter = ('status',)
