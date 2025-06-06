"""
ViewSet для студентов
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import QuerySet

from dojoflow.models import Student
from ..serializers.student import (
    StudentListSerializer, 
    StudentDetailSerializer, 
    StudentCreateUpdateSerializer
)
from ..services.student import StudentService
from ..permissions.student import StudentPermission
from ..filters import StudentFilter
from ..pagination import StandardResultsSetPagination


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления студентами
    """
    permission_classes = [IsAuthenticated, StudentPermission]
    pagination_class = StandardResultsSetPagination
    filterset_class = StudentFilter
    
    def get_queryset(self) -> QuerySet[Student]:
        """Возвращает студентов с учетом прав доступа"""
        club_id = self.request.query_params.get('club')
        return StudentService.get_user_students(
            user=self.request.user,
            club_id=int(club_id) if club_id else None
        )
    
    def get_serializer_class(self):
        """Возвращает соответствующий сериализатор"""
        if self.action == 'list':
            return StudentListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return StudentCreateUpdateSerializer
        else:
            return StudentDetailSerializer
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Статистика по студентам"""
        club_id = request.query_params.get('club')
        stats = StudentService.get_student_statistics(
            user=request.user,
            club_id=int(club_id) if club_id else None
        )
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def eligible_for_attestation(self, request):
        """Студенты, готовые к аттестации"""
        club_id = request.query_params.get('club')
        students = StudentService.get_students_for_attestation(
            user=request.user,
            club_id=int(club_id) if club_id else None
        )
        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        """Перевод студента в другой клуб"""
        student = self.get_object()
        new_club_id = request.data.get('new_club')
        
        if not new_club_id:
            return Response(
                {'error': 'Не указан ID нового клуба'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from dojoflow.models import Club
            new_club = Club.objects.get(id=new_club_id)
            
            if StudentService.transfer_student(student, new_club, request.user):
                serializer = self.get_serializer(student)
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Не удалось перевести студента'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Club.DoesNotExist:
            return Response(
                {'error': 'Клуб не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def attestations(self, request, pk=None):
        """История аттестаций студента"""
        student = self.get_object()
        history = StudentService.get_student_attestation_history(student)
        return Response(history) 