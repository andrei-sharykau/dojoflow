"""
Сериализаторы для уровней аттестации
"""
from rest_framework import serializers
from dojoflow.models import AttestationLevel


class AttestationLevelSerializer(serializers.ModelSerializer):
    """
    Сериализатор для уровней аттестации
    """
    display_name = serializers.CharField(
        source='get_level_display', 
        read_only=True
    )
    students_count = serializers.SerializerMethodField()
    next_level = serializers.SerializerMethodField()
    previous_level = serializers.SerializerMethodField()
    
    class Meta:
        model = AttestationLevel
        fields = [
            'id', 'level', 'display_name', 'order', 'students_count',
            'next_level', 'previous_level'
        ]
        read_only_fields = ['id']
    
    def get_students_count(self, obj):
        """Возвращает количество студентов с данным уровнем"""
        return obj.students.count()
    
    def get_next_level(self, obj):
        """Возвращает следующий уровень"""
        try:
            next_level = AttestationLevel.objects.filter(
                order__gt=obj.order
            ).order_by('order').first()
            
            if next_level:
                return {
                    'id': next_level.id,
                    'level': next_level.level,
                    'display_name': next_level.get_level_display(),
                    'order': next_level.order
                }
        except AttestationLevel.DoesNotExist:
            pass
        return None
    
    def get_previous_level(self, obj):
        """Возвращает предыдущий уровень"""
        try:
            previous_level = AttestationLevel.objects.filter(
                order__lt=obj.order
            ).order_by('-order').first()
            
            if previous_level:
                return {
                    'id': previous_level.id,
                    'level': previous_level.level,
                    'display_name': previous_level.get_level_display(),
                    'order': previous_level.order
                }
        except AttestationLevel.DoesNotExist:
            pass
        return None 