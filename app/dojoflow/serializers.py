from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Club, AttestationLevel, Student, Attestation, ClubAdmin


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ClubSerializer(serializers.ModelSerializer):
    students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Club
        fields = ['id', 'name', 'city', 'created_at', 'students_count']
    
    def get_students_count(self, obj):
        return obj.students.count()


class AttestationLevelSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='get_level_display', read_only=True)
    
    class Meta:
        model = AttestationLevel
        fields = ['id', 'level', 'display_name', 'order']


class AttestationSerializer(serializers.ModelSerializer):
    participants_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Attestation
        fields = ['id', 'date', 'city', 'participants_count', 'created_at']
    
    def get_participants_count(self, obj):
        return obj.participants.count()


class StudentListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка студентов"""
    club_name = serializers.CharField(source='club.name', read_only=True)
    current_level = serializers.SerializerMethodField()
    current_level_display = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    years_of_practice = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'last_name', 'first_name', 'middle_name', 'full_name',
            'club', 'club_name', 'current_level', 'current_level_display',
            'birth_date', 'age', 'years_of_practice', 'city', 'phone', 
            'start_date', 'last_attestation_date', 'created_at'
        ]
    
    def get_current_level(self, obj):
        """Возвращает ID текущего уровня"""
        return obj.current_level.id if obj.current_level else None
    
    def get_current_level_display(self, obj):
        """Возвращает отображаемое название уровня"""
        return obj.current_level.get_level_display() if obj.current_level else None
    
    def get_age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
    
    def get_years_of_practice(self, obj):
        """Вычисляет количество лет занятий"""
        from datetime import date
        today = date.today()
        years = today.year - obj.start_date.year
        if (today.month, today.day) < (obj.start_date.month, obj.start_date.day):
            years -= 1
        return max(0, years)


class StudentDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для студента"""
    club_name = serializers.CharField(source='club.name', read_only=True)
    current_level = serializers.SerializerMethodField()
    current_level_display = serializers.SerializerMethodField()
    attestations = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    years_of_practice = serializers.SerializerMethodField()
    next_attestation_eligible = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'club', 'club_name', 'last_name', 'first_name', 'middle_name', 'full_name',
            'birth_date', 'age', 'years_of_practice', 'city', 'address', 'phone', 'workplace',
            'start_date', 'current_level', 'current_level_display', 'last_attestation_date',
            'attestations', 'next_attestation_eligible', 'created_at', 'updated_at'
        ]
    
    def get_current_level(self, obj):
        """Возвращает ID текущего уровня"""
        return obj.current_level.id if obj.current_level else None
    
    def get_current_level_display(self, obj):
        """Возвращает отображаемое название уровня"""
        return obj.current_level.get_level_display() if obj.current_level else None
    
    def get_age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
    
    def get_years_of_practice(self, obj):
        """Вычисляет количество лет занятий"""
        from datetime import date
        today = date.today()
        years = today.year - obj.start_date.year
        if (today.month, today.day) < (obj.start_date.month, obj.start_date.day):
            years -= 1
        return max(0, years)
    
    def get_attestations(self, obj):
        """Возвращает историю аттестаций студента с деталями уровней"""
        student_attestations = obj.student_attestations.select_related('attestation', 'level').order_by('-attestation__date')
        result = []
        for student_attestation in student_attestations:
            result.append({
                'id': student_attestation.attestation.id,
                'date': student_attestation.attestation.date,
                'city': student_attestation.attestation.city,
                'level': {
                    'id': student_attestation.level.id,
                    'display_name': student_attestation.level.get_level_display()
                }
            })
        return result
    
    def get_next_attestation_eligible(self, obj):
        """Определяет, может ли студент сдавать следующую аттестацию"""
        if not obj.current_level:
            return {
                'eligible': True,
                'next_level': None,
                'reason': 'Студент может сдать на любой уровень'
            }
        
        # Ищем следующий уровень
        try:
            next_level = AttestationLevel.objects.filter(
                order__gt=obj.current_level.order
            ).order_by('order').first()
            
            if not next_level:
                return {
                    'eligible': False,
                    'next_level': None,
                    'reason': 'Достигнут максимальный уровень'
                }
            
            # Проверяем минимальное время между аттестациями (например, 6 месяцев)
            if obj.last_attestation_date:
                from datetime import date, timedelta
                min_date = obj.last_attestation_date + timedelta(days=180)  # 6 месяцев
                if date.today() < min_date:
                    return {
                        'eligible': False,
                        'next_level': next_level.get_level_display(),
                        'reason': f'Следующая аттестация возможна после {min_date.strftime("%d.%m.%Y")}'
                    }
            
            return {
                'eligible': True,
                'next_level': next_level.get_level_display(),
                'reason': 'Студент может сдавать на следующий уровень'
            }
            
        except AttestationLevel.DoesNotExist:
            return {
                'eligible': False,
                'next_level': None,
                'reason': 'Уровни аттестации не настроены'
            }


class StudentCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления студента"""
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'club', 'last_name', 'first_name', 'middle_name', 'full_name',
            'birth_date', 'city', 'address', 'phone', 'workplace',
            'start_date'
        ]
    
    def validate_club(self, value):
        """Проверяем, что пользователь может управлять этим клубом"""
        user = self.context['request'].user
        if user.is_superuser:
            return value
        
        user_clubs = Club.objects.filter(admins__user=user)
        if value not in user_clubs:
            raise serializers.ValidationError("У вас нет прав для управления этим клубом")
        return value


class ClubAdminSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    club_name = serializers.CharField(source='club.name', read_only=True)
    
    class Meta:
        model = ClubAdmin
        fields = ['id', 'user', 'user_name', 'club', 'club_name'] 