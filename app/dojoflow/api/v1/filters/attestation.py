"""
Фильтры для аттестаций
"""
import django_filters
from dojoflow.models import Attestation, Student, Club, AttestationLevel


class AttestationFilter(django_filters.FilterSet):
    """
    Фильтр для аттестаций
    """
    # Фильтр по студенту
    student = django_filters.ModelChoiceFilter(
        queryset=Student.objects.all(),
        label='Студент'
    )
    
    # Фильтр по клубу студента
    club = django_filters.ModelChoiceFilter(
        field_name='student__club',
        queryset=Club.objects.all(),
        label='Клуб'
    )
    
    # Фильтр по уровню аттестации
    level = django_filters.ModelChoiceFilter(
        queryset=AttestationLevel.objects.all(),
        label='Уровень аттестации'
    )
    
    # Фильтр по дате аттестации
    date_from = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        label='Дата аттестации от'
    )
    date_to = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        label='Дата аттестации до'
    )
    
    # Фильтр по городу проведения
    city = django_filters.CharFilter(
        field_name='city',
        lookup_expr='icontains',
        label='Город проведения'
    )
    
    # Поиск по имени студента
    student_search = django_filters.CharFilter(
        method='filter_student_search',
        label='Поиск студента'
    )

    class Meta:
        model = Attestation
        fields = ['student', 'level', 'date', 'city']

    def filter_student_search(self, queryset, name, value):
        """
        Поиск по имени студента
        """
        if value:
            return queryset.filter(
                django_filters.Q(student__last_name__icontains=value) |
                django_filters.Q(student__first_name__icontains=value) |
                django_filters.Q(student__middle_name__icontains=value)
            )
        return queryset 