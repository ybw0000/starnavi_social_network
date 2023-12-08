from rest_framework import serializers

from user.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """Create user request serializer"""

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'])
        return user


class TokenObtainPairResponseSerializer(serializers.Serializer):
    """JWT tokens response schema"""
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenRefreshResponseSerializer(serializers.Serializer):
    """JWT tokens response schema"""
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('last_login', 'last_request')
