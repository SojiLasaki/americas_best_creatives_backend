from django.contrib import admin
from .models import Quote, QuoteInputValue, QuoteDocument


class QuoteInputValueInline(admin.TabularInline):
    model = QuoteInputValue
    extra = 0


class QuoteDocumentInline(admin.TabularInline):
    model = QuoteDocument
    extra = 0


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'catalog', 'station', 'status', 'created_at')
    list_filter = ('status', 'station')
    search_fields = ('customer__email',)
    inlines = [QuoteInputValueInline, QuoteDocumentInline]
