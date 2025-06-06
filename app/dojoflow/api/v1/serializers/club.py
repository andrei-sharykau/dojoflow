"""
Сериализаторы для клубов
"""
from rest_framework import serializers
from dojoflow.models import Club, ClubAdmin
from .student import StudentListSerializer


class ClubSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для клуба
    """
    students_count = serializers.SerializerMethodField()
    admins_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Club
        fields = [
            'id', 'name', 'city', 'address', 'phone', 'email',
            'created_at', 'updated_at', 'students_count', 'admins_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_students_count(self, obj):
        """Возвращает количество студентов в клубе"""
        return obj.students.count()
    
    def get_admins_count(self, obj):
        """Возвращает количество администраторов клуба"""
        return obj.admins.count()


class ClubDetailSerializer(ClubSerializer):
    """
    Детальный сериализатор для клуба
    """
    admins = serializers.SerializerMethodField()
    recent_students = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()
    
    class Meta(ClubSerializer.Meta):
        fields = ClubSerializer.Meta.fields + [
            'admins', 'recent_students', 'statistics'
        ]
    
    def get_admins(self, obj):
        """Возвращает список администраторов клуба"""
        from .auth import UserSerializer
        admins = obj.admins.select_related('user').all()
        return [
            {
                'id': admin.id,
                'user': UserSerializer(admin.user).data,
                'created_at': admin.created_at
            }
            for admin in admins
        ]
    
    def get_recent_students(self, obj):
        """Возвращает последних добавленных студентов"""
        recent_students = obj.students.order_by('-created_at')[:5]
        return StudentListSerializer(recent_students, many=True).data
    
    def get_statistics(self, obj):
        """Возвращает статистику по клубу"""
        students = obj.students.all()
        
        if not students:
            return {
                'total_students': 0,
                'by_level': {},
                'by_age_group': {},
                'avg_age': 0
            }
        
        from datetime import date
        from collections import defaultdict
        
        today = date.today()
        level_stats = defaultdict(int)
        age_groups = defaultdict(int)
        total_age = 0
        
        for student in students:
            # Статистика по уровням
            if student.current_level:
                level_stats[student.current_level.get_level_display()] += 1
            
            # Статистика по возрастным группам
            age = today.year - student.birth_date.year - ((today.month, today.day) < (student.birth_date.month, student.birth_date.day))
            total_age += age
            
            if age < 18:
                age_groups['Дети (до 18)'] += 1
            elif age < 30:
                age_groups['Молодежь (18-30)'] += 1
            elif age < 50:
                age_groups['Взрослые (30-50)'] += 1
            else:
                age_groups['Старшая группа (50+)'] += 1
        
        return {
            'total_students': len(students),
            'by_level': dict(level_stats),
            'by_age_group': dict(age_groups),
            'avg_age': round(total_age / len(students), 1) if students else 0
        }


class ClubWithStudentsSerializer(serializers.ModelSerializer):
    """
    Сериализатор клуба со списком студентов
    """
    students = StudentListSerializer(many=True, read_only=True)
    students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Club
        fields = ['id', 'name', 'city', 'students_count', 'students']
    
    def get_students_count(self, obj):
        """Возвращает количество студентов"""
        return obj.students.count()


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