"""
Сериализаторы для аутентификации
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'full_name']
        read_only_fields = ['id']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username


class LoginSerializer(serializers.Serializer):
    """
    Сериализатор для входа в систему
    """
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )

            if not user:
                msg = 'Неверные учетные данные'
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_active:
                msg = 'Учетная запись отключена'
                raise serializers.ValidationError(msg, code='authorization')

            attrs['user'] = user
            return attrs
        else:
            msg = 'Необходимо указать имя пользователя и пароль'
            raise serializers.ValidationError(msg, code='authorization') 