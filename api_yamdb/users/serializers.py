import re

from rest_framework import serializers, validators
from rest_framework.generics import get_object_or_404

from .models import User


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть me')
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                'Имя может содержать буквы, цифры, символы + @/./+/-/_'
            )
        return value


class UserOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def update(self, instance, validated_data):
        user = get_object_or_404(User, username=instance)
        if user.role != 'admin' and 'role' in validated_data:
            validated_data.pop('role')
        return super().update(instance, validated_data)
