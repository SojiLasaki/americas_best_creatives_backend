from rest_framework import serializers
from .models import Catalog, CatalogInputField


class CatalogInputFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogInputField
        fields = ('id', 'label', 'field_key', 'field_type', 'required', 'options', 'order')


class CatalogSerializer(serializers.ModelSerializer):
    fields = CatalogInputFieldSerializer(many=True, read_only=True)

    class Meta:
        model = Catalog
        fields = ('id', 'name', 'slug', 'description', 'category', 'active', 'fields')
