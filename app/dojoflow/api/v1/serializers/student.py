"""
Сериализаторы для студентов
"""
from rest_framework import serializers
from datetime import date
from dojoflow.models import Student, Club, ClubAdmin, AttestationLevel


class StudentListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка студентов
    """
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
        """Вычисляет возраст студента"""
        today = date.today()
        return today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
    
    def get_years_of_practice(self, obj):
        """Вычисляет количество лет занятий"""
        today = date.today()
        years = today.year - obj.start_date.year
        if (today.month, today.day) < (obj.start_date.month, obj.start_date.day):
            years -= 1
        return max(0, years)


class StudentDetailSerializer(serializers.ModelSerializer):
    """
    Детальный сериализатор для студента
    """
    club_name = serializers.CharField(source='club.name', read_only=True)
    current_level = serializers.SerializerMethodField()
    current_level_display = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    years_of_practice = serializers.SerializerMethodField()
    attestations = serializers.SerializerMethodField()
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
        """Вычисляет возраст студента"""
        today = date.today()
        return today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
    
    def get_years_of_practice(self, obj):
        """Вычисляет количество лет занятий"""
        today = date.today()
        years = today.year - obj.start_date.year
        if (today.month, today.day) < (obj.start_date.month, obj.start_date.day):
            years -= 1
        return max(0, years)
    
    def get_attestations(self, obj):
        """Возвращает историю аттестаций студента"""
        from .attestation import AttestationSerializer
        attestations = obj.attestations.select_related('level').order_by('-date')
        return AttestationSerializer(attestations, many=True).data
    
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
                from datetime import timedelta
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
    """
    Сериализатор для создания/обновления студента
    """
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'club', 'last_name', 'first_name', 'middle_name', 'full_name',
            'birth_date', 'city', 'address', 'phone', 'workplace',
            'start_date'
        ]
    
    def validate_birth_date(self, value):
        """Проверяем корректность даты рождения"""
        today = date.today()
        if value > today:
            raise serializers.ValidationError("Дата рождения не может быть в будущем")
        
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 3:
            raise serializers.ValidationError("Минимальный возраст студента - 3 года")
        if age > 100:
            raise serializers.ValidationError("Максимальный возраст студента - 100 лет")
        
        return value
    
    def validate_start_date(self, value):
        """Проверяем корректность даты начала занятий"""
        today = date.today()
        if value > today:
            raise serializers.ValidationError("Дата начала занятий не может быть в будущем")
        return value
    
    def validate_phone(self, value):
        """Проверяем формат телефона"""
        if value:
            # Удаляем все символы кроме цифр
            digits_only = ''.join(filter(str.isdigit, value))
            if len(digits_only) < 10:
                raise serializers.ValidationError("Номер телефона должен содержать минимум 10 цифр")
        return value
    
    def validate_club(self, value):
        """Проверяем права на управление клубом"""
        user = self.context['request'].user
        if user.is_superuser:
            return value
        
        from dojoflow.models import ClubAdmin
        user_clubs = Club.objects.filter(admins__user=user)
        if value not in user_clubs:
            raise serializers.ValidationError("У вас нет прав для управления этим клубом")
        return value
    
    def validate(self, attrs):
        """Комплексная валидация"""
        birth_date = attrs.get('birth_date')
        start_date = attrs.get('start_date')
        
        if birth_date and start_date:
            # Проверяем, что студент начал заниматься после рождения
            min_start_age = 3  # минимальный возраст начала занятий
            min_start_date = date(
                birth_date.year + min_start_age,
                birth_date.month,
                birth_date.day
            )
            
            if start_date < min_start_date:
                raise serializers.ValidationError(
                    f"Дата начала занятий не может быть раньше {min_start_date.strftime('%d.%m.%Y')} "
                    f"(минимальный возраст начала занятий - {min_start_age} года)"
                )
        
        return attrs 