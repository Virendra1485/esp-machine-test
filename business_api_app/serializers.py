import secrets
from rest_framework import serializers
from .models import Business


class BusinessSerializer(serializers.ModelSerializer):
    api_key = serializers.CharField(read_only=True)
    secret_key = serializers.CharField(read_only=True)

    class Meta:
        model = Business
        fields = ['name', 'registration_number', 'email', 'phone', 'address', 'api_key', 'secret_key']

    def create(self, validated_data):
        # Generate API key and secret
        api_key = secrets.token_hex(16)
        secret_key = secrets.token_urlsafe(32)

        # Create the business
        business = Business.objects.create(api_key=api_key, secret_key=secret_key, **validated_data)
        return business


class BusinessListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = "__all__"
