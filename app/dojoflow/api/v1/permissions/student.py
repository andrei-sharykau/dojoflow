"""
Разрешения для операций со студентами
"""

from rest_framework import permissions
from dojoflow.models import ClubAdmin, Club


class StudentPermission(permissions.BasePermission):
    """
    Разрешения для операций со студентами
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        # Только администраторы клубов могут работать со студентами
        return ClubAdmin.objects.filter(user=request.user).exists()
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        # Проверяем, является ли пользователь администратором клуба студента
        return ClubAdmin.objects.filter(user=request.user, club=obj.club).exists()
    
    def can_create_in_club(self, user, club):
        """
        Проверяет, может ли пользователь создавать студентов в указанном клубе
        """
        if user.is_superuser:
            return True
        
        return ClubAdmin.objects.filter(user=user, club=club).exists()
    
    def can_transfer_student(self, user, student, new_club):
        """
        Проверяет, может ли пользователь перевести студента в новый клуб
        """
        if user.is_superuser:
            return True
        
        # Пользователь должен быть администратором обоих клубов
        user_clubs = Club.objects.filter(admins__user=user)
        return (
            student.club in user_clubs and 
            new_club in user_clubs
        ) 