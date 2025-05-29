"""
Сервис для работы с клубами
"""
from typing import List, Optional, QuerySet
from django.contrib.auth.models import User
from django.db.models import Count, Q, Prefetch
from dojoflow.models import Club, ClubAdmin, Student


class ClubService:
    """
    Сервис для работы с клубами
    """
    
    @staticmethod
    def get_user_clubs(user: User) -> QuerySet[Club]:
        """
        Получает клубы, доступные пользователю
        """
        if user.is_superuser:
            return Club.objects.all()
        
        return Club.objects.filter(admins__user=user)
    
    @staticmethod
    def get_club_with_stats(club_id: int, user: User) -> Optional[Club]:
        """
        Получает клуб с статистикой
        """
        queryset = ClubService.get_user_clubs(user)
        
        try:
            return queryset.select_related().prefetch_related(
                'admins__user',
                Prefetch(
                    'students',
                    queryset=Student.objects.select_related(
                        'current_level'
                    ).prefetch_related('attestations')
                )
            ).annotate(
                students_count=Count('students'),
                admins_count=Count('admins')
            ).get(id=club_id)
        except Club.DoesNotExist:
            return None
    
    @staticmethod
    def get_clubs_with_students(user: User) -> List[dict]:
        """
        Получает клубы со студентами для пользователя
        """
        clubs = ClubService.get_user_clubs(user).prefetch_related(
            Prefetch(
                'students',
                queryset=Student.objects.select_related(
                    'current_level', 'club'
                ).order_by('last_name', 'first_name')
            )
        )
        
        result = []
        for club in clubs:
            club_data = {
                'id': club.id,
                'name': club.name,
                'city': club.city,
                'created_at': club.created_at,
                'students_count': club.students.count(),
                'students': list(club.students.all())
            }
            result.append(club_data)
        
        return result
    
    @staticmethod
    def search_students_in_clubs(user: User, search_query: str = None) -> List[dict]:
        """
        Поиск студентов в клубах пользователя
        """
        clubs_data = ClubService.get_clubs_with_students(user)
        
        if search_query:
            # Фильтруем студентов по поисковому запросу
            for club_data in clubs_data:
                filtered_students = []
                for student in club_data['students']:
                    if (search_query.lower() in student.full_name.lower() or
                        search_query.lower() in (student.phone or '').lower()):
                        filtered_students.append(student)
                
                club_data['students'] = filtered_students
                club_data['students_count'] = len(filtered_students)
        
        return clubs_data
    
    @staticmethod
    def can_user_manage_club(user: User, club: Club) -> bool:
        """
        Проверяет, может ли пользователь управлять клубом
        """
        if user.is_superuser:
            return True
        
        return ClubAdmin.objects.filter(user=user, club=club).exists()
    
    @staticmethod
    def get_club_statistics(club: Club) -> dict:
        """
        Получает статистику по клубу
        """
        from django.db.models import Avg
        from datetime import date, timedelta
        
        students = club.students.all()
        total_students = students.count()
        
        if total_students == 0:
            return {
                'total_students': 0,
                'average_age': 0,
                'new_students_this_month': 0,
                'students_by_level': {},
                'recent_attestations': 0
            }
        
        # Средний возраст
        today = date.today()
        ages = [
            today.year - student.birth_date.year - 
            ((today.month, today.day) < (student.birth_date.month, student.birth_date.day))
            for student in students if student.birth_date
        ]
        average_age = sum(ages) / len(ages) if ages else 0
        
        # Новые студенты за месяц
        month_ago = today - timedelta(days=30)
        new_students_this_month = students.filter(created_at__gte=month_ago).count()
        
        # Распределение по уровням
        students_by_level = {}
        for student in students:
            if student.current_level:
                level_name = student.current_level.get_level_display()
                students_by_level[level_name] = students_by_level.get(level_name, 0) + 1
        
        # Аттестации за месяц
        from dojoflow.models import Attestation
        recent_attestations = Attestation.objects.filter(
            student__club=club,
            date__gte=month_ago
        ).count()
        
        return {
            'total_students': total_students,
            'average_age': round(average_age, 1),
            'new_students_this_month': new_students_this_month,
            'students_by_level': students_by_level,
            'recent_attestations': recent_attestations
        } 