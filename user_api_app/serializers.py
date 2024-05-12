from rest_framework import serializers
from .models import User
import secrets


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'phone', 'password', 'email', 'address']

    def create(self, validated_data):
        user = User.objects.create_user(
            name=validated_data.get('name', ''),
            phone=validated_data['phone'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            address=validated_data['address'],
            api_key=secrets.token_hex(16),
            secret_key=secrets.token_urlsafe(32),
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone', 'email', 'address']
        read_only_fields = ['phone']  # Make phone read-only to prevent accidental changes

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance


class TokenRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)
    password = serializers.CharField(required=True)


class UserDeletionSerializer(serializers.Serializer):
    def validate(self, attrs):
        token = self.context['request'].headers.get('Authorization', '').split(' ')[1]
        attrs['token'] = token
        return attrs
