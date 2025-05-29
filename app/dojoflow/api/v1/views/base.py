"""
Базовые классы для API views
"""
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from dojoflow.api.v1.pagination import StandardResultsSetPagination
from dojoflow.api.v1.permissions import IsClubAdminOrSuperuser
from dojoflow.utils.mixins import UserClubMixin, PermissionCheckMixin


class BaseAPIViewSet(viewsets.ModelViewSet, UserClubMixin, PermissionCheckMixin):
    """
    Базовый ViewSet для всех API endpoints
    """
    permission_classes = [permissions.IsAuthenticated, IsClubAdminOrSuperuser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    def get_queryset(self):
        """
        Фильтрует queryset по правам пользователя
        """
        queryset = super().get_queryset()
        return self.filter_by_user_clubs(queryset, self.request.user)
    
    def perform_create(self, serializer):
        """
        Добавляет дополнительную логику при создании объекта
        """
        serializer.save()
    
    def perform_update(self, serializer):
        """
        Добавляет дополнительную логику при обновлении объекта
        """
        serializer.save()
    
    def handle_exception(self, exc):
        """
        Обрабатывает исключения и возвращает подходящие HTTP ответы
        """
        from dojoflow.utils.exceptions import DojoFlowException
        
        if isinstance(exc, DojoFlowException):
            return Response(
                {'error': exc.message, 'code': exc.code},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().handle_exception(exc)
    
    @action(detail=False, methods=['get'])
    def count(self, request):
        """
        Возвращает количество объектов
        """
        queryset = self.filter_queryset(self.get_queryset())
        return Response({'count': queryset.count()})


class ReadOnlyAPIViewSet(viewsets.ReadOnlyModelViewSet, UserClubMixin):
    """
    Базовый ViewSet только для чтения
    """
    permission_classes = [permissions.IsAuthenticated, IsClubAdminOrSuperuser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    def get_queryset(self):
        """
        Фильтрует queryset по правам пользователя
        """
        queryset = super().get_queryset()
        return self.filter_by_user_clubs(queryset, self.request.user) 