"""
Базовые разрешения для API
"""
from rest_framework import permissions
from dojoflow.models import ClubAdmin


class IsClubAdminOrSuperuser(permissions.BasePermission):
    """
    Разрешение для администраторов клубов и суперпользователей
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        # Проверяем, является ли пользователь администратором хотя бы одного клуба
        return ClubAdmin.objects.filter(user=request.user).exists()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение для редактирования только владельцем объекта
    """
    def has_object_permission(self, request, view, obj):
        # Разрешения на чтение предоставляются для любого запроса,
        # поэтому мы всегда разрешаем GET, HEAD или OPTIONS запросы.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешения на запись предоставляются только владельцу объекта.
        return obj.owner == request.user


class IsClubMember(permissions.BasePermission):
    """
    Разрешение для участников клуба
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Суперпользователи имеют доступ ко всему
        if request.user.is_superuser:
            return True
        
        # Проверяем, является ли пользователь членом хотя бы одного клуба
        return ClubAdmin.objects.filter(user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        # Проверяем доступ к объекту в зависимости от его типа
        if hasattr(obj, 'club'):
            # Для объектов связанных с клубом (Student, Attestation)
            user_clubs = ClubAdmin.objects.filter(user=request.user).values_list('club', flat=True)
            return obj.club.id in user_clubs
        elif hasattr(obj, 'admins'):
            # Для самих клубов
            return ClubAdmin.objects.filter(user=request.user, club=obj).exists()
        
        return False 