"""
Сериализаторы для студентов
"""
from rest_framework import serializers
from datetime import date
from dojoflow.models import Student, Club, ClubAdmin


class StudentListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка студентов
    """
    club_name = serializers.CharField(source='club.name', read_only=True)
    current_level_display = serializers.CharField(
        source='current_level.get_level_display', 
        read_only=True
    )
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'last_name', 'first_name', 'middle_name', 'full_name',
            'club', 'club_name', 'current_level', 'current_level_display',
            'birth_date', 'age', 'city', 'phone', 'start_date', 'last_attestation_date'
        ]
    
    def get_age(self, obj):
        """Вычисляет возраст студента"""
        if not obj.birth_date:
            return None
        today = date.today()
        return (today.year - obj.birth_date.year - 
                ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day)))


class StudentDetailSerializer(StudentListSerializer):
    """
    Детальный сериализатор для студента
    """
    attestations = serializers.SerializerMethodField()
    attestations_count = serializers.SerializerMethodField()
    years_of_practice = serializers.SerializerMethodField()
    
    class Meta(StudentListSerializer.Meta):
        fields = StudentListSerializer.Meta.fields + [
            'address', 'workplace', 'attestations', 'attestations_count',
            'years_of_practice', 'created_at', 'updated_at'
        ]
    
    def get_attestations(self, obj):
        """Возвращает аттестации студента"""
        # Импорт внутри метода для избежания циклических импортов
        from .attestation import AttestationSerializer
        attestations = obj.attestations.order_by('-date')
        return AttestationSerializer(attestations, many=True, context=self.context).data
    
    def get_attestations_count(self, obj):
        """Возвращает количество аттестаций"""
        return obj.attestations.count()
    
    def get_years_of_practice(self, obj):
        """Вычисляет количество лет практики"""
        if not obj.start_date:
            return None
        today = date.today()
        years = today.year - obj.start_date.year
        if (today.month, today.day) < (obj.start_date.month, obj.start_date.day):
            years -= 1
        return max(0, years)


class StudentCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания/обновления студента
    """
    
    class Meta:
        model = Student
        fields = [
            'club', 'last_name', 'first_name', 'middle_name',
            'birth_date', 'city', 'address', 'phone', 'workplace',
            'start_date', 'current_level', 'last_attestation_date'
        ]
    
    def validate_club(self, value):
        """Проверяем, что пользователь может управлять этим клубом"""
        user = self.context['request'].user
        if user.is_superuser:
            return value
        
        user_clubs = Club.objects.filter(admins__user=user)
        if value not in user_clubs:
            raise serializers.ValidationError(
                "У вас нет прав для управления этим клубом"
            )
        return value
    
    def validate_birth_date(self, value):
        """Проверяем дату рождения"""
        if value and value > date.today():
            raise serializers.ValidationError(
                "Дата рождения не может быть в будущем"
            )
        return value
    
    def validate_start_date(self, value):
        """Проверяем дату начала занятий"""
        if value and value > date.today():
            raise serializers.ValidationError(
                "Дата начала занятий не может быть в будущем"
            )
        return value
    
    def validate_last_attestation_date(self, value):
        """Проверяем дату последней аттестации"""
        if value and value > date.today():
            raise serializers.ValidationError(
                "Дата аттестации не может быть в будущем"
            )
        
        # Проверяем, что дата аттестации не раньше даты начала занятий
        start_date = self.initial_data.get('start_date')
        if start_date and value and value < start_date:
            raise serializers.ValidationError(
                "Дата аттестации не может быть раньше даты начала занятий"
            )
        return value 