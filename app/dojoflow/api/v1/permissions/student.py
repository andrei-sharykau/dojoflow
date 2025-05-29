"""
Разрешения для работы со студентами
"""
from rest_framework import permissions
from dojoflow.models import ClubAdmin


class StudentPermission(permissions.BasePermission):
    """
    Разрешение для работы со студентами
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        # Администраторы клубов могут работать со студентами своих клубов
        return ClubAdmin.objects.filter(user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        # Проверяем, является ли пользователь администратором клуба студента
        return ClubAdmin.objects.filter(
            user=request.user, 
            club=obj.club
        ).exists() 