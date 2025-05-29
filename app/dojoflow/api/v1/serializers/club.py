"""
Сериализаторы для клубов
"""
from rest_framework import serializers
from dojoflow.models import Club, ClubAdmin
from .student import StudentListSerializer


class ClubSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор клуба
    """
    students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Club
        fields = ['id', 'name', 'city', 'created_at', 'students_count']
        read_only_fields = ['id', 'created_at']
    
    def get_students_count(self, obj):
        """Возвращает количество студентов в клубе"""
        return obj.students.count()


class ClubDetailSerializer(ClubSerializer):
    """
    Детальный сериализатор клуба
    """
    recent_students = serializers.SerializerMethodField()
    admins_count = serializers.SerializerMethodField()
    
    class Meta(ClubSerializer.Meta):
        fields = ClubSerializer.Meta.fields + [
            'recent_students', 'admins_count', 'updated_at'
        ]
    
    def get_recent_students(self, obj):
        """Возвращает последних добавленных студентов"""
        recent = obj.students.order_by('-created_at')[:5]
        return StudentListSerializer(recent, many=True, context=self.context).data
    
    def get_admins_count(self, obj):
        """Возвращает количество администраторов клуба"""
        return obj.admins.count()


class ClubWithStudentsSerializer(ClubSerializer):
    """
    Сериализатор клуба со всеми студентами
    """
    students = StudentListSerializer(many=True, read_only=True)
    
    class Meta(ClubSerializer.Meta):
        fields = ClubSerializer.Meta.fields + ['students']


class ClubAdminSerializer(serializers.ModelSerializer):
    """
    Сериализатор администратора клуба
    """
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    club_name = serializers.CharField(source='club.name', read_only=True)
    
    class Meta:
        model = ClubAdmin
        fields = ['id', 'user', 'user_name', 'user_username', 'club', 'club_name']
        read_only_fields = ['id']