"""
Сервис для работы с клубами
"""

from django.db.models import Q, Count, Avg
from django.contrib.auth.models import User
from dojoflow.models import Club, ClubAdmin, Student
from datetime import date
from typing import List, Dict, Optional


class ClubService:
    """
    Сервис для работы с клубами
    """
    
    @staticmethod
    def get_user_clubs(user: User) -> List[Club]:
        """
        Возвращает клубы, к которым имеет доступ пользователь
        """
        if user.is_superuser:
            return Club.objects.all()
        
        return Club.objects.filter(admins__user=user).distinct()
    
    @staticmethod
    def get_club_statistics(club: Club) -> Dict:
        """
        Возвращает статистику по клубу
        """
        students = club.students.all()
        
        if not students:
            return {
                'total_students': 0,
                'avg_age': 0,
                'by_level': {},
                'by_age_group': {},
                'recent_joiners': 0,
                'active_students': 0
            }
        
        today = date.today()
        
        # Базовая статистика
        total_students = students.count()
        
        # Средний возраст
        ages = []
        level_stats = {}
        age_groups = {
            'Дети (до 18)': 0,
            'Молодежь (18-30)': 0,
            'Взрослые (30-50)': 0,
            'Старшая группа (50+)': 0
        }
        
        for student in students:
            # Возраст
            age = today.year - student.birth_date.year - (
                (today.month, today.day) < (student.birth_date.month, student.birth_date.day)
            )
            ages.append(age)
            
            # Группировка по возрасту
            if age < 18:
                age_groups['Дети (до 18)'] += 1
            elif age < 30:
                age_groups['Молодежь (18-30)'] += 1
            elif age < 50:
                age_groups['Взрослые (30-50)'] += 1
            else:
                age_groups['Старшая группа (50+)'] += 1
            
            # Статистика по уровням
            if student.current_level:
                level_name = student.current_level.get_level_display()
                level_stats[level_name] = level_stats.get(level_name, 0) + 1
        
        # Новые студенты (за последние 30 дней)
        from datetime import timedelta
        recent_date = today - timedelta(days=30)
        recent_joiners = students.filter(start_date__gte=recent_date).count()
        
        # Активные студенты (те, кто проходил аттестацию в последние 6 месяцев)
        active_date = today - timedelta(days=180)
        # Не можем использовать last_attestation_date в фильтре, так как это property
        # Считаем активных студентов через цикл
        active_students = 0
        for student in students:
            if student.last_attestation_date and student.last_attestation_date >= active_date:
                active_students += 1
        
        return {
            'total_students': total_students,
            'avg_age': round(sum(ages) / len(ages), 1) if ages else 0,
            'by_level': level_stats,
            'by_age_group': age_groups,
            'recent_joiners': recent_joiners,
            'active_students': active_students
        }
    
    @staticmethod
    def search_students_in_club(club: Club, search_query: str) -> List[Student]:
        """
        Поиск студентов в клубе
        """
        students = club.students.all()
        
        if search_query:
            students = students.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(middle_name__icontains=search_query) |
                Q(phone__icontains=search_query)
            )
        
        return students.order_by('last_name', 'first_name')
    
    @staticmethod
    def can_user_manage_club(user: User, club: Club) -> bool:
        """
        Проверяет, может ли пользователь управлять клубом
        """
        if user.is_superuser:
            return True
        
        return ClubAdmin.objects.filter(user=user, club=club).exists()
    
    @staticmethod
    def get_clubs_with_students(user: User, search_query: Optional[str] = None) -> List[Dict]:
        """
        Возвращает клубы со списком студентов
        """
        clubs = ClubService.get_user_clubs(user)
        result = []
        
        for club in clubs:
            students = ClubService.search_students_in_club(club, search_query)
            
            club_data = {
                'id': club.id,
                'name': club.name,
                'city': club.city,
                'students_count': students.count(),
                'students': []  # Будем заполнять вручную
            }
            
            # Добавляем возраст для каждого студента
            today = date.today()
            for student in club_data['students']:
                if student['birth_date']:
                    birth_date = student['birth_date']
                    age = today.year - birth_date.year - (
                        (today.month, today.day) < (birth_date.month, birth_date.day)
                    )
                    student['age'] = age
                else:
                    student['age'] = None
            
            result.append(club_data)
        
        return result
    
    @staticmethod
    def get_club_permissions(user: User, club: Club) -> Dict:
        """
        Возвращает права пользователя на клуб
        """
        if user.is_superuser:
            return {
                'can_view': True,
                'can_edit': True,
                'can_delete': True,
                'can_manage_students': True,
                'can_manage_admins': True,
                'role': 'superuser'
            }
        
        is_admin = ClubAdmin.objects.filter(user=user, club=club).exists()
        
        return {
            'can_view': is_admin,
            'can_edit': is_admin,
            'can_delete': False,  # Только суперпользователи могут удалять клубы
            'can_manage_students': is_admin,
            'can_manage_admins': False,  # Только суперпользователи могут управлять администраторами
            'role': 'admin' if is_admin else 'none'
        } 