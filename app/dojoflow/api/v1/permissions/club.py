"""
Разрешения для операций с клубами
"""
from rest_framework import permissions
from dojoflow.models import ClubAdmin


class ClubPermission(permissions.BasePermission):
    """
    Разрешения для операций с клубами
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        # Только администраторы клубов могут работать с клубами
        return ClubAdmin.objects.filter(user=request.user).exists()
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        # Проверяем, является ли пользователь администратором данного клуба
        return ClubAdmin.objects.filter(user=request.user, club=obj).exists() 