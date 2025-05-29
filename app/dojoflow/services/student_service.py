"""
Сервис для работы со студентами
"""
from typing import List, Optional, QuerySet, Dict, Any
from django.contrib.auth.models import User
from django.db.models import Q, Prefetch, Count
from django.core.exceptions import PermissionDenied
from datetime import date, timedelta
from dojoflow.models import Student, Club, ClubAdmin, Attestation


class StudentService:
    """
    Сервис для работы со студентами
    """
    
    @staticmethod
    def get_user_students(user: User) -> QuerySet[Student]:
        """
        Получает студентов, доступных пользователю
        """
        if user.is_superuser:
            return Student.objects.all()
        
        user_clubs = ClubAdmin.objects.filter(user=user).values_list('club', flat=True)
        return Student.objects.filter(club__in=user_clubs)
    
    @staticmethod
    def get_students_with_details(user: User) -> QuerySet[Student]:
        """
        Получает студентов с подробной информацией
        """
        return StudentService.get_user_students(user).select_related(
            'club', 'current_level'
        ).prefetch_related(
            Prefetch(
                'attestations',
                queryset=Attestation.objects.select_related('level').order_by('-date')
            )
        ).order_by('last_name', 'first_name')
    
    @staticmethod
    def search_students(user: User, query: str) -> QuerySet[Student]:
        """
        Поиск студентов по различным критериям
        """
        students = StudentService.get_user_students(user)
        
        if not query:
            return students
        
        return students.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(phone__icontains=query)
        )
    
    @staticmethod
    def get_student_by_id(student_id: int, user: User) -> Optional[Student]:
        """
        Получает студента по ID с проверкой прав доступа
        """
        try:
            return StudentService.get_students_with_details(user).get(id=student_id)
        except Student.DoesNotExist:
            return None
    
    @staticmethod
    def can_user_manage_student(user: User, student: Student) -> bool:
        """
        Проверяет, может ли пользователь управлять студентом
        """
        if user.is_superuser:
            return True
        
        return ClubAdmin.objects.filter(user=user, club=student.club).exists()
    
    @staticmethod
    def create_student(user: User, student_data: Dict[str, Any]) -> Student:
        """
        Создает нового студента
        """
        club = student_data.get('club')
        
        # Проверяем права на управление клубом
        if not user.is_superuser:
            user_clubs = Club.objects.filter(admins__user=user)
            if club not in user_clubs:
                raise PermissionDenied("У вас нет прав для управления этим клубом")
        
        return Student.objects.create(**student_data)
    
    @staticmethod
    def update_student(user: User, student: Student, student_data: Dict[str, Any]) -> Student:
        """
        Обновляет данные студента
        """
        if not StudentService.can_user_manage_student(user, student):
            raise PermissionDenied("У вас нет прав для управления этим студентом")
        
        # Если меняется клуб, проверяем права на новый клуб
        new_club = student_data.get('club')
        if new_club and new_club != student.club:
            if not user.is_superuser:
                user_clubs = Club.objects.filter(admins__user=user)
                if new_club not in user_clubs:
                    raise PermissionDenied("У вас нет прав для перевода в этот клуб")
        
        # Обновляем поля
        for field, value in student_data.items():
            setattr(student, field, value)
        
        student.save()
        return student
    
    @staticmethod
    def delete_student(user: User, student: Student) -> bool:
        """
        Удаляет студента
        """
        if not StudentService.can_user_manage_student(user, student):
            raise PermissionDenied("У вас нет прав для удаления этого студента")
        
        student.delete()
        return True
    
    @staticmethod
    def get_student_statistics(student: Student) -> Dict[str, Any]:
        """
        Получает статистику по студенту
        """
        attestations = student.attestations.all().order_by('date')
        
        # Базовая информация
        today = date.today()
        age = None
        years_of_practice = None
        
        if student.birth_date:
            age = today.year - student.birth_date.year - (
                (today.month, today.day) < (student.birth_date.month, student.birth_date.day)
            )
        
        if student.start_date:
            years_of_practice = today.year - student.start_date.year - (
                (today.month, today.day) < (student.start_date.month, student.start_date.day)
            )
            years_of_practice = max(0, years_of_practice)
        
        # Статистика аттестаций
        total_attestations = attestations.count()
        last_attestation = attestations.last()
        
        # Прогресс по уровням
        attestation_timeline = []
        for attestation in attestations:
            attestation_timeline.append({
                'date': attestation.date,
                'level': attestation.level.get_level_display(),
                'city': attestation.city,
                'notes': attestation.notes
            })
        
        return {
            'age': age,
            'years_of_practice': years_of_practice,
            'total_attestations': total_attestations,
            'last_attestation_date': last_attestation.date if last_attestation else None,
            'last_attestation_level': last_attestation.level.get_level_display() if last_attestation else None,
            'attestation_timeline': attestation_timeline,
            'current_level': student.current_level.get_level_display() if student.current_level else None
        }
    
    @staticmethod
    def get_club_students_with_filter(
        user: User, 
        club_id: Optional[int] = None, 
        search: Optional[str] = None,
        level_id: Optional[int] = None
    ) -> QuerySet[Student]:
        """
        Получает студентов клуба с фильтрацией
        """
        students = StudentService.get_students_with_details(user)
        
        # Фильтр по клубу
        if club_id:
            # Проверяем доступ к клубу
            if not user.is_superuser:
                user_clubs = ClubAdmin.objects.filter(user=user).values_list('club', flat=True)
                if club_id not in user_clubs:
                    return Student.objects.none()
            
            students = students.filter(club_id=club_id)
        
        # Поиск по тексту
        if search:
            students = students.filter(
                Q(last_name__icontains=search) |
                Q(first_name__icontains=search) |
                Q(middle_name__icontains=search) |
                Q(phone__icontains=search)
            )
        
        # Фильтр по уровню
        if level_id:
            students = students.filter(current_level_id=level_id)
        
        return students
    
    @staticmethod
    def get_students_for_attestation(user: User, club_id: Optional[int] = None) -> QuerySet[Student]:
        """
        Получает студентов, готовых к аттестации
        """
        students = StudentService.get_students_with_details(user)
        
        if club_id:
            students = students.filter(club_id=club_id)
        
        # Фильтруем студентов, которые занимаются больше 6 месяцев
        six_months_ago = date.today() - timedelta(days=180)
        students = students.filter(start_date__lte=six_months_ago)
        
        return students.order_by('current_level__order', 'last_name') 