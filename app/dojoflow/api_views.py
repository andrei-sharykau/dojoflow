from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Club, AttestationLevel, Student, Attestation, ClubAdmin
from .serializers import (
    ClubSerializer, AttestationLevelSerializer, StudentListSerializer,
    StudentDetailSerializer, StudentCreateUpdateSerializer, AttestationSerializer,
    UserSerializer, ClubAdminSerializer
)


class IsClubAdminOrSuperuser(permissions.BasePermission):
    """
    Разрешение для администраторов клубов и суперпользователей
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        # Проверяем, является ли пользователь администратором хотя бы одного клуба
        return ClubAdmin.objects.filter(user=request.user).exists()


class ClubViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для клубов. Пользователи видят только свои клубы.
    """
    serializer_class = ClubSerializer
    permission_classes = [IsClubAdminOrSuperuser]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Club.objects.all()
        
        # Возвращаем только клубы, которыми управляет пользователь
        return Club.objects.filter(admins__user=user).distinct()
    
    @action(detail=False, methods=['get'])
    def students_by_club(self, request):
        """Получить список занимающихся в разрезе клуба"""
        clubs = self.get_queryset()
        result = []
        
        for club in clubs:
            students = club.students.select_related('current_level').order_by('last_name', 'first_name')
            
            # Применяем поиск если указан
            search = request.query_params.get('search', None)
            if search:
                students = students.filter(
                    Q(last_name__icontains=search) |
                    Q(first_name__icontains=search) |
                    Q(middle_name__icontains=search) |
                    Q(phone__icontains=search)
                )
            
            club_data = {
                'id': club.id,
                'name': club.name,
                'city': club.city,
                'students_count': students.count(),
                'students': StudentListSerializer(students, many=True).data
            }
            result.append(club_data)
        
        return Response(result)


class AttestationLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для уровней аттестации. Только чтение.
    """
    queryset = AttestationLevel.objects.all()
    serializer_class = AttestationLevelSerializer
    permission_classes = [IsClubAdminOrSuperuser]


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для студентов с учетом прав доступа
    """
    permission_classes = [IsClubAdminOrSuperuser]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = Student.objects.all()
        else:
            # Возвращаем только студентов из клубов пользователя
            user_clubs = Club.objects.filter(admins__user=user)
            queryset = Student.objects.filter(club__in=user_clubs)
        
        # Фильтрация по клубу
        club_id = self.request.query_params.get('club', None)
        if club_id:
            queryset = queryset.filter(club_id=club_id)
        
        # Поиск
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(last_name__icontains=search) |
                Q(first_name__icontains=search) |
                Q(middle_name__icontains=search) |
                Q(phone__icontains=search)
            )
        
        return queryset.select_related('club', 'current_level').order_by('last_name', 'first_name')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return StudentListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return StudentCreateUpdateSerializer
        else:
            return StudentDetailSerializer
    
    def perform_create(self, serializer):
        # Проверяем права при создании
        club = serializer.validated_data['club']
        user = self.request.user
        
        if not user.is_superuser:
            user_clubs = Club.objects.filter(admins__user=user)
            if club not in user_clubs:
                raise permissions.PermissionDenied("У вас нет прав для создания студентов в этом клубе")
        
        serializer.save()
    
    def perform_update(self, serializer):
        # Проверяем права при обновлении
        instance = self.get_object()
        user = self.request.user
        
        if not user.is_superuser:
            user_clubs = Club.objects.filter(admins__user=user)
            if instance.club not in user_clubs:
                raise permissions.PermissionDenied("У вас нет прав для редактирования этого студента")
            
            # Если пытаются изменить клуб, проверяем права на новый клуб
            if 'club' in serializer.validated_data:
                new_club = serializer.validated_data['club']
                if new_club not in user_clubs:
                    raise permissions.PermissionDenied("У вас нет прав для перевода студента в этот клуб")
        
        serializer.save()
    
    @action(detail=True, methods=['get'])
    def attestations(self, request, pk=None):
        """Получить аттестации студента"""
        student = self.get_object()
        attestations = student.attestations.all().select_related('level')
        serializer = AttestationSerializer(attestations, many=True)
        return Response(serializer.data)


class AttestationViewSet(viewsets.ModelViewSet):
    """
    ViewSet для аттестаций
    """
    serializer_class = AttestationSerializer
    permission_classes = [IsClubAdminOrSuperuser]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            queryset = Attestation.objects.all()
        else:
            # Возвращаем только аттестации студентов из клубов пользователя
            user_clubs = Club.objects.filter(admins__user=user)
            queryset = Attestation.objects.filter(student__club__in=user_clubs)
        
        # Фильтрация по студенту
        student_id = self.request.query_params.get('student', None)
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        # Фильтрация по клубу
        club_id = self.request.query_params.get('club', None)
        if club_id:
            queryset = queryset.filter(student__club_id=club_id)
        
        return queryset.select_related('student', 'level', 'student__club').order_by('-date')
    
    def perform_create(self, serializer):
        # Проверяем права при создании
        student = serializer.validated_data['student']
        user = self.request.user
        
        if not user.is_superuser:
            user_clubs = Club.objects.filter(admins__user=user)
            if student.club not in user_clubs:
                raise permissions.PermissionDenied("У вас нет прав для создания аттестаций для этого студента")
        
        serializer.save()


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для профиля пользователя
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Получить информацию о текущем пользователе"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_clubs(self, request):
        """Получить клубы текущего пользователя"""
        user = request.user
        if user.is_superuser:
            clubs = Club.objects.all()
        else:
            clubs = Club.objects.filter(admins__user=user).distinct()
        
        serializer = ClubSerializer(clubs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def permissions(self, request):
        """Получить права пользователя"""
        user = request.user
        return Response({
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            'clubs_count': Club.objects.filter(admins__user=user).count() if not user.is_superuser else Club.objects.count(),
        }) 