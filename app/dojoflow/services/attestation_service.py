"""
Сервис для работы с аттестациями
"""
from typing import List, Optional, QuerySet, Dict, Any
from django.contrib.auth.models import User
from django.db.models import Q, Prefetch, Count
from django.core.exceptions import PermissionDenied, ValidationError
from datetime import date, timedelta
from dojoflow.models import Attestation, Student, Club, ClubAdmin, AttestationLevel


class AttestationService:
    """
    Сервис для работы с аттестациями
    """
    
    @staticmethod
    def get_user_attestations(user: User) -> QuerySet[Attestation]:
        """
        Получает аттестации, доступные пользователю
        """
        if user.is_superuser:
            return Attestation.objects.all()
        
        user_clubs = ClubAdmin.objects.filter(user=user).values_list('club', flat=True)
        return Attestation.objects.filter(student__club__in=user_clubs)
    
    @staticmethod
    def get_attestations_with_details(user: User) -> QuerySet[Attestation]:
        """
        Получает аттестации с подробной информацией
        """
        return AttestationService.get_user_attestations(user).select_related(
            'student', 'student__club', 'level'
        ).order_by('-date', '-created_at')
    
    @staticmethod
    def get_attestation_by_id(attestation_id: int, user: User) -> Optional[Attestation]:
        """
        Получает аттестацию по ID с проверкой прав доступа
        """
        try:
            return AttestationService.get_attestations_with_details(user).get(id=attestation_id)
        except Attestation.DoesNotExist:
            return None
    
    @staticmethod
    def can_user_manage_attestation(user: User, attestation: Attestation) -> bool:
        """
        Проверяет, может ли пользователь управлять аттестацией
        """
        if user.is_superuser:
            return True
        
        return ClubAdmin.objects.filter(
            user=user, 
            club=attestation.student.club
        ).exists()
    
    @staticmethod
    def create_attestation(user: User, attestation_data: Dict[str, Any]) -> Attestation:
        """
        Создает новую аттестацию
        """
        student = attestation_data.get('student')
        level = attestation_data.get('level')
        attestation_date = attestation_data.get('date')
        
        # Проверяем права на управление студентом
        if not user.is_superuser:
            user_clubs = ClubAdmin.objects.filter(user=user).values_list('club', flat=True)
            if student.club.id not in user_clubs:
                raise PermissionDenied("У вас нет прав для работы с этим студентом")
        
        # Валидация бизнес-логики
        AttestationService._validate_attestation_logic(student, level, attestation_date)
        
        attestation = Attestation.objects.create(**attestation_data)
        
        # Обновляем текущий уровень студента, если новый уровень выше
        AttestationService._update_student_level(student, level)
        
        return attestation
    
    @staticmethod
    def update_attestation(
        user: User, 
        attestation: Attestation, 
        attestation_data: Dict[str, Any]
    ) -> Attestation:
        """
        Обновляет аттестацию
        """
        if not AttestationService.can_user_manage_attestation(user, attestation):
            raise PermissionDenied("У вас нет прав для управления этой аттестацией")
        
        student = attestation_data.get('student', attestation.student)
        level = attestation_data.get('level', attestation.level)
        attestation_date = attestation_data.get('date', attestation.date)
        
        # Валидация бизнес-логики
        AttestationService._validate_attestation_logic(
            student, level, attestation_date, exclude_attestation=attestation
        )
        
        # Обновляем поля
        for field, value in attestation_data.items():
            setattr(attestation, field, value)
        
        attestation.save()
        
        # Перепроверяем уровень студента
        AttestationService._recalculate_student_level(student)
        
        return attestation
    
    @staticmethod
    def delete_attestation(user: User, attestation: Attestation) -> bool:
        """
        Удаляет аттестацию
        """
        if not AttestationService.can_user_manage_attestation(user, attestation):
            raise PermissionDenied("У вас нет прав для удаления этой аттестации")
        
        student = attestation.student
        attestation.delete()
        
        # Перепроверяем уровень студента после удаления аттестации
        AttestationService._recalculate_student_level(student)
        
        return True
    
    @staticmethod
    def get_club_attestations(
        user: User,
        club_id: Optional[int] = None,
        level_id: Optional[int] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        search: Optional[str] = None
    ) -> QuerySet[Attestation]:
        """
        Получает аттестации клуба с фильтрацией
        """
        attestations = AttestationService.get_attestations_with_details(user)
        
        # Фильтр по клубу
        if club_id:
            if not user.is_superuser:
                user_clubs = ClubAdmin.objects.filter(user=user).values_list('club', flat=True)
                if club_id not in user_clubs:
                    return Attestation.objects.none()
            
            attestations = attestations.filter(student__club_id=club_id)
        
        # Фильтр по уровню
        if level_id:
            attestations = attestations.filter(level_id=level_id)
        
        # Фильтр по датам
        if date_from:
            attestations = attestations.filter(date__gte=date_from)
        
        if date_to:
            attestations = attestations.filter(date__lte=date_to)
        
        # Поиск по студенту
        if search:
            attestations = attestations.filter(
                Q(student__last_name__icontains=search) |
                Q(student__first_name__icontains=search) |
                Q(student__middle_name__icontains=search)
            )
        
        return attestations
    
    @staticmethod
    def get_attestation_statistics(
        user: User,
        club_id: Optional[int] = None,
        period_days: int = 365
    ) -> Dict[str, Any]:
        """
        Получает статистику по аттестациям
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=period_days)
        
        attestations = AttestationService.get_user_attestations(user).filter(
            date__range=[start_date, end_date]
        )
        
        if club_id:
            attestations = attestations.filter(student__club_id=club_id)
        
        # Общая статистика
        total_attestations = attestations.count()
        
        # Распределение по уровням
        attestations_by_level = {}
        for attestation in attestations.select_related('level'):
            level_name = attestation.level.get_level_display()
            attestations_by_level[level_name] = attestations_by_level.get(level_name, 0) + 1
        
        # Статистика по месяцам
        monthly_stats = {}
        for attestation in attestations:
            month_key = attestation.date.strftime('%Y-%m')
            monthly_stats[month_key] = monthly_stats.get(month_key, 0) + 1
        
        # Топ студентов по количеству аттестаций
        from django.db.models import Count
        top_students = attestations.values(
            'student__last_name', 'student__first_name'
        ).annotate(
            attestation_count=Count('id')
        ).order_by('-attestation_count')[:10]
        
        return {
            'total_attestations': total_attestations,
            'period_days': period_days,
            'attestations_by_level': attestations_by_level,
            'monthly_statistics': monthly_stats,
            'top_students': list(top_students)
        }
    
    @staticmethod
    def _validate_attestation_logic(
        student: Student, 
        level: AttestationLevel, 
        attestation_date: date,
        exclude_attestation: Optional[Attestation] = None
    ) -> None:
        """
        Валидирует бизнес-логику аттестации
        """
        # Проверяем, что дата аттестации не раньше даты начала занятий
        if student.start_date and attestation_date < student.start_date:
            raise ValidationError(
                "Дата аттестации не может быть раньше даты начала занятий студента"
            )
        
        # Проверяем, что нет дублирующих аттестаций на тот же уровень
        existing_query = Attestation.objects.filter(
            student=student,
            level=level
        )
        
        if exclude_attestation:
            existing_query = existing_query.exclude(id=exclude_attestation.id)
        
        if existing_query.exists():
            raise ValidationError("У студента уже есть аттестация на этот уровень")
    
    @staticmethod
    def _update_student_level(student: Student, new_level: AttestationLevel) -> None:
        """
        Обновляет текущий уровень студента, если новый уровень выше
        """
        if not student.current_level or new_level.order > student.current_level.order:
            student.current_level = new_level
            student.last_attestation_date = date.today()
            student.save(update_fields=['current_level', 'last_attestation_date'])
    
    @staticmethod
    def _recalculate_student_level(student: Student) -> None:
        """
        Пересчитывает текущий уровень студента на основе всех его аттестаций
        """
        highest_attestation = student.attestations.select_related('level').order_by(
            '-level__order'
        ).first()
        
        if highest_attestation:
            student.current_level = highest_attestation.level
            # Находим дату последней аттестации этого уровня
            last_attestation = student.attestations.filter(
                level=highest_attestation.level
            ).order_by('-date').first()
            student.last_attestation_date = last_attestation.date
        else:
            student.current_level = None
            student.last_attestation_date = None
        
        student.save(update_fields=['current_level', 'last_attestation_date']) 