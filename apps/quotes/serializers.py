from rest_framework import serializers
from .models import Quote, QuoteInputValue, QuoteDocument
from apps.users.serializers import UserSerializer


class QuoteInputValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteInputValue
        fields = ('id', 'field', 'value')


class QuoteDocumentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = QuoteDocument
        fields = ('id', 'quote', 'uploaded_by', 'file', 'uploaded_at')
        read_only_fields = ('uploaded_by', 'uploaded_at')


class QuoteSerializer(serializers.ModelSerializer):
    input_values = QuoteInputValueSerializer(many=True, read_only=True)
    documents = QuoteDocumentSerializer(many=True, read_only=True)
    customer_email = serializers.CharField(source='customer.email', read_only=True)
    catalog_name = serializers.CharField(source='catalog.name', read_only=True)

    class Meta:
        model = Quote
        fields = (
            'id', 'customer', 'customer_email', 'station', 'catalog', 'catalog_name',
            'created_by_agent', 'status', 'submitted_snapshot', 'created_at', 'updated_at',
            'input_values', 'documents',
        )
        read_only_fields = ('customer', 'created_by_agent', 'created_at', 'updated_at')


class QuoteCreateSerializer(serializers.ModelSerializer):
    input_values = QuoteInputValueSerializer(many=True, required=False)

    class Meta:
        model = Quote
        fields = ('catalog', 'station', 'submitted_snapshot', 'input_values')

    def create(self, validated_data):
        input_values_data = validated_data.pop('input_values', [])
        quote = Quote.objects.create(**validated_data)
        for iv in input_values_data:
            QuoteInputValue.objects.create(quote=quote, **iv)
        return quote


class QuoteStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ('status',)
