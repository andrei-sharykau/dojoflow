"""
Фильтры для студентов
"""
import django_filters
from dojoflow.models import Student, Club, AttestationLevel


class StudentFilter(django_filters.FilterSet):
    """
    Фильтр для студентов
    """
    # Поиск по тексту
    search = django_filters.CharFilter(method='filter_search', label='Поиск')
    
    # Фильтр по клубу
    club = django_filters.ModelChoiceFilter(
        queryset=Club.objects.all(),
        label='Клуб'
    )
    
    # Фильтр по городу
    city = django_filters.CharFilter(
        field_name='city',
        lookup_expr='icontains',
        label='Город'
    )
    
    # Фильтр по уровню аттестации
    current_level = django_filters.ModelChoiceFilter(
        queryset=AttestationLevel.objects.all(),
        label='Текущий уровень'
    )
    
    # Фильтр по диапазону возраста
    age_from = django_filters.NumberFilter(
        method='filter_age_from',
        label='Возраст от'
    )
    age_to = django_filters.NumberFilter(
        method='filter_age_to',
        label='Возраст до'
    )
    
    # Фильтр по дате начала занятий
    start_date_from = django_filters.DateFilter(
        field_name='start_date',
        lookup_expr='gte',
        label='Начало занятий от'
    )
    start_date_to = django_filters.DateFilter(
        field_name='start_date',
        lookup_expr='lte',
        label='Начало занятий до'
    )

    class Meta:
        model = Student
        fields = {
            'last_name': ['exact', 'icontains'],
            'first_name': ['exact', 'icontains'],
        }

    def filter_search(self, queryset, name, value):
        """
        Поиск по имени, фамилии, отчеству или телефону
        """
        if value:
            return queryset.filter(
                django_filters.Q(last_name__icontains=value) |
                django_filters.Q(first_name__icontains=value) |
                django_filters.Q(middle_name__icontains=value) |
                django_filters.Q(phone__icontains=value)
            )
        return queryset

    def filter_age_from(self, queryset, name, value):
        """
        Фильтр по минимальному возрасту
        """
        if value is not None:
            from django.utils import timezone
            from datetime import date
            
            today = date.today()
            birth_year = today.year - value
            max_birth_date = date(birth_year, today.month, today.day)
            
            return queryset.filter(birth_date__lte=max_birth_date)
        return queryset

    def filter_age_to(self, queryset, name, value):
        """
        Фильтр по максимальному возрасту
        """
        if value is not None:
            from django.utils import timezone
            from datetime import date
            
            today = date.today()
            birth_year = today.year - value - 1
            min_birth_date = date(birth_year, today.month, today.day)
            
            return queryset.filter(birth_date__gte=min_birth_date)
        return queryset 