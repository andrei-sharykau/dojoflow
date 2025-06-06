"""
Сервис для работы со студентами
"""

from django.db.models import Q, Count, Max
from django.contrib.auth.models import User
from dojoflow.models import Student, Club, ClubAdmin, Attestation, AttestationLevel
from datetime import date, timedelta
from typing import List, Dict, Optional
from django.db.models import QuerySet


class StudentService:
    """
    Сервис для работы со студентами
    """
    
    @staticmethod
    def get_user_students(user: User, club_id: Optional[int] = None) -> QuerySet[Student]:
        """
        Возвращает студентов, к которым имеет доступ пользователь
        """
        if user.is_superuser:
            queryset = Student.objects.all()
        else:
            user_clubs = Club.objects.filter(admins__user=user)
            queryset = Student.objects.filter(club__in=user_clubs)
        
        if club_id:
            queryset = queryset.filter(club_id=club_id)
        
        return queryset.select_related('club').order_by('last_name', 'first_name')
    
    @staticmethod
    def search_students(user: User, search_query: str, club_id: Optional[int] = None) -> QuerySet[Student]:
        """
        Поиск студентов с учетом прав доступа
        """
        queryset = StudentService.get_user_students(user, club_id)
        
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(middle_name__icontains=search_query) |
                Q(phone__icontains=search_query)
            )
        
        return queryset
    
    @staticmethod
    def can_user_manage_student(user: User, student: Student) -> bool:
        """
        Проверяет, может ли пользователь управлять студентом
        """
        if user.is_superuser:
            return True
        
        return ClubAdmin.objects.filter(user=user, club=student.club).exists()
    
    @staticmethod
    def can_user_create_student_in_club(user: User, club: Club) -> bool:
        """
        Проверяет, может ли пользователь создавать студентов в клубе
        """
        if user.is_superuser:
            return True
        
        return ClubAdmin.objects.filter(user=user, club=club).exists()
    
    @staticmethod
    def get_student_statistics(user: User, club_id: Optional[int] = None) -> Dict:
        """
        Возвращает статистику по студентам
        """
        students = StudentService.get_user_students(user, club_id)
        
        if not students:
            return {
                'total_students': 0,
                'by_level': {},
                'by_age_group': {},
                'by_city': {},
                'avg_age': 0,
                'avg_years_practice': 0,
                'recent_joiners': 0,
                'need_attestation': 0
            }
        
        today = date.today()
        
        # Базовая статистика
        total_students = students.count()
        
        # Инициализация счетчиков
        level_stats = {}
        age_groups = {
            'Дети (до 18)': 0,
            'Молодежь (18-30)': 0,
            'Взрослые (30-50)': 0,
            'Старшая группа (50+)': 0
        }
        city_stats = {}
        ages = []
        years_practice = []
        
        for student in students:
            # Возраст
            age = today.year - student.birth_date.year - (
                (today.month, today.day) < (student.birth_date.month, student.birth_date.day)
            )
            ages.append(age)
            
            # Годы практики
            practice_years = today.year - student.start_date.year
            if (today.month, today.day) < (student.start_date.month, student.start_date.day):
                practice_years -= 1
            years_practice.append(max(0, practice_years))
            
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
            else:
                level_stats['Без уровня'] = level_stats.get('Без уровня', 0) + 1
            
            # Статистика по городам
            city = student.city or 'Не указан'
            city_stats[city] = city_stats.get(city, 0) + 1
        
        # Новые студенты (за последние 30 дней)
        recent_date = today - timedelta(days=30)
        recent_joiners = students.filter(start_date__gte=recent_date).count()
        
        # Студенты, которым нужна аттестация (не было аттестации больше 6 месяцев)
        attestation_date = today - timedelta(days=180)
        # Не можем использовать last_attestation_date в фильтре, так как это property
        # Считаем через цикл
        need_attestation = 0
        for student in students:
            if not student.last_attestation_date or student.last_attestation_date < attestation_date:
                need_attestation += 1
        
        return {
            'total_students': total_students,
            'by_level': level_stats,
            'by_age_group': age_groups,
            'by_city': city_stats,
            'avg_age': round(sum(ages) / len(ages), 1) if ages else 0,
            'avg_years_practice': round(sum(years_practice) / len(years_practice), 1) if years_practice else 0,
            'recent_joiners': recent_joiners,
            'need_attestation': need_attestation
        }
    
    @staticmethod
    def get_students_for_attestation(user: User, club_id: Optional[int] = None) -> List[Student]:
        """
        Возвращает студентов, готовых к аттестации
        """
        students = StudentService.get_user_students(user, club_id)
        
        today = date.today()
        min_attestation_date = today - timedelta(days=180)  # 6 месяцев
        
        # Студенты, которые могут сдавать аттестацию:
        # 1. Давно не сдавали (больше 6 месяцев)
        # 2. Никогда не сдавали
        # 3. Есть следующий уровень для сдачи
        eligible_students = []
        
        for student in students:
            can_attest = False
            
            # Проверяем время последней аттестации
            if not student.last_attestation_date or student.last_attestation_date < min_attestation_date:
                can_attest = True
            
            # Проверяем, есть ли следующий уровень
            if can_attest and student.current_level:
                next_level = AttestationLevel.objects.filter(
                    order__gt=student.current_level.order
                ).order_by('order').first()
                
                if not next_level:
                    can_attest = False  # Максимальный уровень достигнут
            
            if can_attest:
                eligible_students.append(student)
        
        return eligible_students
    
    @staticmethod
    def get_student_attestation_history(student: Student) -> List[Dict]:
        """
        Возвращает историю аттестаций студента с аналитикой
        """
        attestations = student.attestations.select_related('level').order_by('date')
        
        history = []
        previous_date = student.start_date
        
        for i, attestation in enumerate(attestations):
            # Время между аттестациями
            time_diff = None
            if previous_date:
                delta = attestation.date - previous_date
                time_diff = delta.days
            
            # Прогресс (повышение уровня)
            level_progress = 'new' if i == 0 else 'up'
            if i > 0:
                prev_attestation = attestations[i-1]
                if attestation.level.order <= prev_attestation.level.order:
                    level_progress = 'same' if attestation.level.order == prev_attestation.level.order else 'down'
            
            history.append({
                'id': attestation.id,
                'date': attestation.date,
                'level': {
                    'id': attestation.level.id,
                    'name': attestation.level.get_level_display(),
                    'order': attestation.level.order
                },
                'city': attestation.city,
                'time_since_previous_days': time_diff,
                'level_progress': level_progress,
                'created_at': attestation.created_at
            })
            
            previous_date = attestation.date
        
        return history
    
    @staticmethod
    def validate_student_transfer(user: User, student: Student, new_club: Club) -> bool:
        """
        Проверяет возможность перевода студента в другой клуб
        """
        if user.is_superuser:
            return True
        
        # Пользователь должен быть администратором обоих клубов
        user_clubs = Club.objects.filter(admins__user=user)
        return student.club in user_clubs and new_club in user_clubs
    
    @staticmethod
    def transfer_student(student: Student, new_club: Club, user: User) -> bool:
        """
        Переводит студента в другой клуб
        """
        if not StudentService.validate_student_transfer(user, student, new_club):
            return False
        
        old_club = student.club
        student.club = new_club
        student.save(update_fields=['club'])
        
        # Можно добавить логирование перевода
        # TransferLog.objects.create(
        #     student=student,
        #     from_club=old_club,
        #     to_club=new_club,
        #     transferred_by=user,
        #     transfer_date=date.today()
        # )
        
        return True 