"""
Сериализаторы для уровней аттестации
"""
from rest_framework import serializers
from dojoflow.models import AttestationLevel


class AttestationLevelSerializer(serializers.ModelSerializer):
    """
    Сериализатор уровня аттестации
    """
    display_name = serializers.CharField(
        source='get_level_display', 
        read_only=True
    )
    students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = AttestationLevel
        fields = ['id', 'level', 'display_name', 'order', 'students_count']
        read_only_fields = ['id']
    
    def get_students_count(self, obj):
        """Возвращает количество студентов с данным уровнем"""
        return obj.students.count() 