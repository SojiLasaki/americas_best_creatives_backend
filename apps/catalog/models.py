from django.db import models
from django.utils.text import slugify


class Catalog(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CatalogInputField(models.Model):
    class FieldType(models.TextChoices):
        TEXT = 'text', 'Text'
        NUMBER = 'number', 'Number'
        SELECT = 'select', 'Select'
        BOOLEAN = 'boolean', 'Boolean'
        FILE = 'file', 'File'
        TEXTAREA = 'textarea', 'Textarea'

    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(max_length=255)
    field_key = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FieldType.choices, default=FieldType.TEXT)
    required = models.BooleanField(default=False)
    options = models.JSONField(default=list, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('catalog', 'field_key')

    def __str__(self):
        return f'{self.catalog.name} - {self.label}'
