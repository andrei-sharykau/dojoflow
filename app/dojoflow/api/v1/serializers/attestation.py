"""
Сериализаторы для аттестаций
"""
from rest_framework import serializers
from datetime import date
from dojoflow.models import Attestation, Student, ClubAdmin, AttestationLevel


class AttestationSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для аттестации
    """
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    level_display = serializers.CharField(source='level.get_level_display', read_only=True)
    club_name = serializers.CharField(source='student.club.name', read_only=True)
    
    class Meta:
        model = Attestation
        fields = [
            'id', 'student', 'student_name', 'level', 'level_display',
            'club_name', 'date', 'city', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AttestationDetailSerializer(serializers.ModelSerializer):
    """
    Детальный сериализатор для аттестации
    """
    student_info = serializers.SerializerMethodField()
    level_info = serializers.SerializerMethodField()
    attestation_context = serializers.SerializerMethodField()
    
    class Meta:
        model = Attestation
        fields = [
            'id', 'student', 'student_info', 'level', 'level_info',
            'date', 'city', 'attestation_context', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_student_info(self, obj):
        """Возвращает подробную информацию о студенте"""
        student = obj.student
        from datetime import date
        today = date.today()
        age = today.year - student.birth_date.year - ((today.month, today.day) < (student.birth_date.month, student.birth_date.day))
        
        return {
            'id': student.id,
            'full_name': student.full_name,
            'age': age,
            'club': student.club.name,
            'start_date': student.start_date,
            'phone': student.phone,
            'city': student.city
        }
    
    def get_level_info(self, obj):
        """Возвращает информацию об уровне"""
        level = obj.level
        return {
            'id': level.id,
            'level': level.level,
            'display_name': level.get_level_display(),
            'order': level.order
        }
    
    def get_attestation_context(self, obj):
        """Возвращает контекст аттестации"""
        student = obj.student
        
        # Предыдущие аттестации
        previous_attestations = student.attestations.filter(
            date__lt=obj.date
        ).order_by('-date')[:3]
        
        # Следующие аттестации
        next_attestations = student.attestations.filter(
            date__gt=obj.date
        ).order_by('date')[:3]
        
        # Время между аттестациями
        time_since_start = None
        time_since_previous = None
        
        if student.start_date:
            delta = obj.date - student.start_date
            time_since_start = delta.days
        
        if previous_attestations:
            delta = obj.date - previous_attestations[0].date
            time_since_previous = delta.days
        
        return {
            'time_since_start_days': time_since_start,
            'time_since_previous_days': time_since_previous,
            'previous_attestations': [
                {
                    'date': att.date,
                    'level': att.level.get_level_display(),
                    'city': att.city
                }
                for att in previous_attestations
            ],
            'next_attestations': [
                {
                    'date': att.date,
                    'level': att.level.get_level_display(),
                    'city': att.city
                }
                for att in next_attestations
            ]
        }


class AttestationCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания/обновления аттестации
    """
    
    class Meta:
        model = Attestation
        fields = ['student', 'level', 'date', 'city']
    
    def validate_date(self, value):
        """Проверяем корректность даты аттестации"""
        if value > date.today():
            raise serializers.ValidationError("Дата аттестации не может быть в будущем")
        return value
    
    def validate_student(self, value):
        """Проверяем права на работу со студентом"""
        user = self.context['request'].user
        if user.is_superuser:
            return value
        
        from dojoflow.models import ClubAdmin, Club
        user_clubs = Club.objects.filter(admins__user=user)
        if value.club not in user_clubs:
            raise serializers.ValidationError("У вас нет прав для работы с этим студентом")
        return value
    
    def validate(self, attrs):
        """Комплексная валидация аттестации"""
        student = attrs.get('student')
        level = attrs.get('level')
        attestation_date = attrs.get('date')
        
        if student and attestation_date:
            # Проверяем, что дата аттестации не раньше даты начала занятий
            if attestation_date < student.start_date:
                raise serializers.ValidationError(
                    "Дата аттестации не может быть раньше даты начала занятий студента"
                )
            
            # Проверяем на дублирование аттестации
            existing_attestation = Attestation.objects.filter(
                student=student,
                level=level,
                date=attestation_date
            )
            
            # Исключаем текущую аттестацию при обновлении
            if self.instance:
                existing_attestation = existing_attestation.exclude(id=self.instance.id)
            
            if existing_attestation.exists():
                raise serializers.ValidationError(
                    "Аттестация на этот уровень в эту дату уже существует"
                )
            
            # Проверяем логическую последовательность уровней
            if level and student.current_level:
                if level.order <= student.current_level.order:
                    # Разрешаем аттестацию на тот же уровень только если это переаттестация
                    if level.order == student.current_level.order:
                        # Проверяем, есть ли уже аттестация на этот уровень
                        existing_same_level = student.attestations.filter(level=level)
                        if self.instance:
                            existing_same_level = existing_same_level.exclude(id=self.instance.id)
                        
                        if existing_same_level.exists():
                            raise serializers.ValidationError(
                                "Студент уже имеет аттестацию на этот уровень"
                            )
                    else:
                        raise serializers.ValidationError(
                            "Нельзя сдавать аттестацию на уровень ниже текущего"
                        )
            
            # Проверяем минимальное время между аттестациями (например, 3 месяца)
            last_attestation = student.attestations.order_by('-date').first()
            if self.instance:
                last_attestation = student.attestations.exclude(id=self.instance.id).order_by('-date').first()
            
            if last_attestation:
                from datetime import timedelta
                min_interval = timedelta(days=90)  # 3 месяца
                if attestation_date - last_attestation.date < min_interval:
                    raise serializers.ValidationError(
                        f"Минимальный интервал между аттестациями - 3 месяца. "
                        f"Следующая аттестация возможна после {(last_attestation.date + min_interval).strftime('%d.%m.%Y')}"
                    )
        
        return attrs
    
    def create(self, validated_data):
        """Создание аттестации с обновлением текущего уровня студента"""
        attestation = super().create(validated_data)
        
        # Обновляем текущий уровень студента (current_level и last_attestation_date - это @property)
        # Они вычисляются автоматически из связанных аттестаций
        pass
        
        return attestation
    
    def update(self, instance, validated_data):
        """Обновление аттестации с проверкой текущего уровня студента"""
        old_level = instance.level
        old_date = instance.date
        
        attestation = super().update(instance, validated_data)
        
        # Если изменился уровень или дата, то current_level и last_attestation_date
        # обновятся автоматически, так как это @property
        pass
        
        return attestation 