"""
Сериализаторы для аутентификации
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from dojoflow.models import ClubAdmin


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя
    """
    clubs_count = serializers.SerializerMethodField()
    is_club_admin = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_superuser', 'is_staff', 'date_joined', 'last_login',
            'clubs_count', 'is_club_admin'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def get_clubs_count(self, obj):
        """Возвращает количество клубов пользователя"""
        if obj.is_superuser:
            from dojoflow.models import Club
            return Club.objects.count()
        return ClubAdmin.objects.filter(user=obj).count()
    
    def get_is_club_admin(self, obj):
        """Проверяет, является ли пользователь администратором клуба"""
        return ClubAdmin.objects.filter(user=obj).exists()


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
                raise serializers.ValidationError(
                    'Неверное имя пользователя или пароль',
                    code='authorization'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    'Аккаунт пользователя отключен',
                    code='authorization'
                )
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Необходимо указать имя пользователя и пароль',
                code='authorization'
            ) 