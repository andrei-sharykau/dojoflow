"""
Сериализаторы для аттестаций
"""
from rest_framework import serializers
from datetime import date
from dojoflow.models import Attestation, Student, ClubAdmin


class AttestationSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор аттестации
    """
    level_display = serializers.CharField(
        source='level.get_level_display', 
        read_only=True
    )
    student_name = serializers.CharField(
        source='student.full_name', 
        read_only=True
    )
    club_name = serializers.CharField(
        source='student.club.name', 
        read_only=True
    )
    
    class Meta:
        model = Attestation
        fields = [
            'id', 'student', 'student_name', 'club_name',
            'level', 'level_display', 'date', 'city', 
            'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AttestationCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания/обновления аттестации
    """
    
    class Meta:
        model = Attestation
        fields = ['student', 'level', 'date', 'city', 'notes']
    
    def validate_student(self, value):
        """Проверяем, что пользователь может управлять студентом"""
        user = self.context['request'].user
        if user.is_superuser:
            return value
        
        # Проверяем, что студент принадлежит к клубу администратора
        user_clubs = ClubAdmin.objects.filter(user=user).values_list('club', flat=True)
        if value.club.id not in user_clubs:
            raise serializers.ValidationError(
                "У вас нет прав для работы с этим студентом"
            )
        return value
    
    def validate_date(self, value):
        """Проверяем дату аттестации"""
        if value and value > date.today():
            raise serializers.ValidationError(
                "Дата аттестации не может быть в будущем"
            )
        return value
    
    def validate(self, attrs):
        """Общая валидация"""
        student = attrs.get('student')
        level = attrs.get('level')
        attestation_date = attrs.get('date')
        
        # Если это обновление, получаем оригинальный объект
        if self.instance:
            student = student or self.instance.student
            level = level or self.instance.level
            attestation_date = attestation_date or self.instance.date
        
        # Проверяем, что дата аттестации не раньше даты начала занятий
        if student and student.start_date and attestation_date:
            if attestation_date < student.start_date:
                raise serializers.ValidationError({
                    'date': 'Дата аттестации не может быть раньше даты начала занятий студента'
                })
        
        # Проверяем, что нет дублирующих аттестаций на тот же уровень
        if student and level:
            existing_query = Attestation.objects.filter(
                student=student,
                level=level
            )
            
            # Если это обновление, исключаем текущий объект
            if self.instance:
                existing_query = existing_query.exclude(id=self.instance.id)
            
            if existing_query.exists():
                raise serializers.ValidationError({
                    'level': 'У студента уже есть аттестация на этот уровень'
                })
        
        return attrs 