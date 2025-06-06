"""
Фильтры для API v1
"""

import django_filters
from django.db.models import Q
from dojoflow.models import Student, Attestation, Club
from datetime import date


class StudentFilter(django_filters.FilterSet):
    """
    Фильтр для студентов
    """
    search = django_filters.CharFilter(method='filter_search', label='Поиск')
    club = django_filters.ModelChoiceFilter(queryset=Club.objects.all(), label='Клуб')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains', label='Город')
    level = django_filters.NumberFilter(field_name='current_level__level', label='Уровень')
    
    # Фильтры по возрасту
    min_age = django_filters.NumberFilter(method='filter_min_age', label='Минимальный возраст')
    max_age = django_filters.NumberFilter(method='filter_max_age', label='Максимальный возраст')
    
    # Фильтры по датам
    start_date_after = django_filters.DateFilter(field_name='start_date', lookup_expr='gte', label='Начал заниматься после')
    start_date_before = django_filters.DateFilter(field_name='start_date', lookup_expr='lte', label='Начал заниматься до')
    
    class Meta:
        model = Student
        fields = ['club', 'city', 'current_level']
    
    def filter_search(self, queryset, name, value):
        """
        Поиск по имени, фамилии, отчеству и телефону
        """
        if value:
            return queryset.filter(
                Q(first_name__icontains=value) |
                Q(last_name__icontains=value) |
                Q(middle_name__icontains=value) |
                Q(phone__icontains=value)
            )
        return queryset
    
    def filter_min_age(self, queryset, name, value):
        """
        Фильтр по минимальному возрасту
        """
        if value:
            today = date.today()
            max_birth_date = date(today.year - value, today.month, today.day)
            return queryset.filter(birth_date__lte=max_birth_date)
        return queryset
    
    def filter_max_age(self, queryset, name, value):
        """
        Фильтр по максимальному возрасту
        """
        if value:
            today = date.today()
            min_birth_date = date(today.year - value - 1, today.month, today.day)
            return queryset.filter(birth_date__gte=min_birth_date)
        return queryset


class AttestationFilter(django_filters.FilterSet):
    """
    Фильтр для аттестаций
    """
    search = django_filters.CharFilter(method='filter_search', label='Поиск')
    student = django_filters.ModelChoiceFilter(queryset=Student.objects.all(), label='Студент')
    club = django_filters.ModelChoiceFilter(queryset=Club.objects.all(), label='Клуб')
    level = django_filters.NumberFilter(field_name='level__level', label='Уровень')
    
    # Фильтры по датам
    date_after = django_filters.DateFilter(field_name='date', lookup_expr='gte', label='После даты')
    date_before = django_filters.DateFilter(field_name='date', lookup_expr='lte', label='До даты')
    
    # Фильтр по городу
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains', label='Город')
    
    class Meta:
        model = Attestation
        fields = ['student', 'club', 'level', 'city']
    
    def filter_search(self, queryset, name, value):
        """
        Поиск по студентам и городу
        """
        if value:
            return queryset.filter(
                Q(student__first_name__icontains=value) |
                Q(student__last_name__icontains=value) |
                Q(student__middle_name__icontains=value) |
                Q(city__icontains=value)
            )
        return queryset 