from django.contrib import admin
from .models import Catalog, CatalogInputField


class CatalogInputFieldInline(admin.TabularInline):
    model = CatalogInputField
    extra = 1


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'active')
    list_filter = ('active', 'category')
    search_fields = ('name', 'slug')
    inlines = [CatalogInputFieldInline]


@admin.register(CatalogInputField)
class CatalogInputFieldAdmin(admin.ModelAdmin):
    list_display = ('catalog', 'label', 'field_key', 'field_type', 'required', 'order')
    list_filter = ('field_type', 'required')
