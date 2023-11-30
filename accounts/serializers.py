from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )
    password_confirmation = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirmation')
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirmation': {'write_only': True}
        }

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        if (password and password_confirmation
                and password != password_confirmation):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation', None)
        user = User.objects.create_user(**validated_data)
        return user
