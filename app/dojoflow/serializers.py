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
    level_display = serializers.CharField(source='level.get_level_display', read_only=True)
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    
    class Meta:
        model = Attestation
        fields = ['id', 'student', 'student_name', 'level', 'level_display', 'date', 'city', 'notes', 'created_at']


class StudentListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка студентов"""
    club_name = serializers.CharField(source='club.name', read_only=True)
    current_level_display = serializers.CharField(source='current_level.get_level_display', read_only=True)
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'last_name', 'first_name', 'middle_name', 'full_name',
            'club', 'club_name', 'current_level', 'current_level_display',
            'birth_date', 'age', 'city', 'phone', 'start_date', 'last_attestation_date'
        ]
    
    def get_age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))


class StudentDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для студента"""
    club_name = serializers.CharField(source='club.name', read_only=True)
    current_level_display = serializers.CharField(source='current_level.get_level_display', read_only=True)
    attestations = AttestationSerializer(many=True, read_only=True)
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'club', 'club_name', 'last_name', 'first_name', 'middle_name', 'full_name',
            'birth_date', 'age', 'city', 'address', 'phone', 'workplace',
            'start_date', 'current_level', 'current_level_display', 'last_attestation_date',
            'attestations', 'created_at', 'updated_at'
        ]
    
    def get_age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))


class StudentCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/обновления студента"""
    
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
            raise serializers.ValidationError("У вас нет прав для управления этим клубом")
        return value


class ClubAdminSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    club_name = serializers.CharField(source='club.name', read_only=True)
    
    class Meta:
        model = ClubAdmin
        fields = ['id', 'user', 'user_name', 'club', 'club_name'] 