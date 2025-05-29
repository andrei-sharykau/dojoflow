"""
Разрешения для работы с клубами
"""
from rest_framework import permissions
from dojoflow.models import ClubAdmin


class ClubPermission(permissions.BasePermission):
    """
    Разрешение для работы с клубами
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Суперпользователи имеют полный доступ
        if request.user.is_superuser:
            return True
        
        # Администраторы клубов могут просматривать свои клубы
        if request.method in permissions.SAFE_METHODS:
            return ClubAdmin.objects.filter(user=request.user).exists()
        
        # Создание и изменение клубов только для суперпользователей
        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        # Администраторы могут просматривать только свои клубы
        if request.method in permissions.SAFE_METHODS:
            return ClubAdmin.objects.filter(user=request.user, club=obj).exists()
        
        # Изменение и удаление только для суперпользователей
        return False 