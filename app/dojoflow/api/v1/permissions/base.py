"""
Базовые классы разрешений для API v1
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
    Разрешение, которое позволяет только владельцам объекта редактировать его
    """
    def has_object_permission(self, request, view, obj):
        # Разрешения на чтение для всех аутентифицированных пользователей
        if request.method in permissions.SAFE_METHODS:
            return True

        # Права на запись только для владельца объекта
        return obj.owner == request.user


class IsClubMember(permissions.BasePermission):
    """
    Разрешение для членов клуба (студентов и администраторов)
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        # Проверяем, является ли пользователь администратором или студентом клуба
        return ClubAdmin.objects.filter(user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        # Получаем клуб из объекта
        club = getattr(obj, 'club', None)
        if not club:
            return False
        
        # Проверяем, является ли пользователь администратором этого клуба
        return ClubAdmin.objects.filter(user=request.user, club=club).exists() 