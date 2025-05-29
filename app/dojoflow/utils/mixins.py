"""
Миксины для view и сериализаторов
"""
from typing import QuerySet
from django.contrib.auth.models import User
from rest_framework.request import Request
from dojoflow.models import ClubAdmin


class UserClubMixin:
    """
    Миксин для фильтрации по клубам пользователя
    """
    
    def get_user_clubs_queryset(self, user: User) -> QuerySet:
        """
        Возвращает queryset клубов, доступных пользователю
        """
        from dojoflow.models import Club
        
        if user.is_superuser:
            return Club.objects.all()
        
        return Club.objects.filter(admins__user=user)
    
    def filter_by_user_clubs(self, queryset: QuerySet, user: User) -> QuerySet:
        """
        Фильтрует queryset по клубам пользователя
        """
        if user.is_superuser:
            return queryset
        
        user_clubs = ClubAdmin.objects.filter(user=user).values_list('club', flat=True)
        
        # Определяем поле для фильтрации в зависимости от модели
        if hasattr(queryset.model, 'club'):
            return queryset.filter(club__in=user_clubs)
        elif hasattr(queryset.model, 'student'):
            return queryset.filter(student__club__in=user_clubs)
        elif queryset.model.__name__ == 'Club':
            return queryset.filter(id__in=user_clubs)
        
        return queryset
    
    def can_user_access_club(self, user: User, club_id: int) -> bool:
        """
        Проверяет, может ли пользователь получить доступ к клубу
        """
        if user.is_superuser:
            return True
        
        return ClubAdmin.objects.filter(user=user, club_id=club_id).exists()


class TimestampMixin:
    """
    Миксин для добавления информации о временных метках
    """
    
    def add_timestamp_info(self, data: dict) -> dict:
        """
        Добавляет информацию о создании и обновлении
        """
        if hasattr(self, 'created_at'):
            data['created_at'] = self.created_at
        
        if hasattr(self, 'updated_at'):
            data['updated_at'] = self.updated_at
        
        return data


class PermissionCheckMixin:
    """
    Миксин для проверки разрешений
    """
    
    def check_club_permission(self, request: Request, club_id: int) -> bool:
        """
        Проверяет разрешение на доступ к клубу
        """
        user = request.user
        
        if not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True
        
        return ClubAdmin.objects.filter(user=user, club_id=club_id).exists()
    
    def check_student_permission(self, request: Request, student) -> bool:
        """
        Проверяет разрешение на доступ к студенту
        """
        user = request.user
        
        if not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True
        
        return ClubAdmin.objects.filter(user=user, club=student.club).exists()
    
    def check_attestation_permission(self, request: Request, attestation) -> bool:
        """
        Проверяет разрешение на доступ к аттестации
        """
        user = request.user
        
        if not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True
        
        return ClubAdmin.objects.filter(
            user=user, 
            club=attestation.student.club
        ).exists()