from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Club, AttestationLevel, Student, Attestation, ClubAdmin


@admin.register(Club)
class ClubModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'created_at']
    list_filter = ['city', 'created_at']
    search_fields = ['name', 'city']
    ordering = ['city', 'name']


@admin.register(AttestationLevel)
class AttestationLevelAdmin(admin.ModelAdmin):
    list_display = ['level', 'get_level_display', 'order']
    ordering = ['order']
    
    def has_add_permission(self, request):
        # Запрещаем добавление новых уровней - они фиксированы
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление уровней
        return request.user.is_superuser


class AttestationInline(admin.TabularInline):
    model = Attestation
    extra = 0
    fields = ['level', 'date', 'city', 'notes']
    ordering = ['-date']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'last_name', 'first_name', 'middle_name', 
        'club', 'current_level', 'start_date', 'last_attestation_date'
    ]
    list_filter = ['club', 'current_level', 'city', 'start_date']
    search_fields = ['last_name', 'first_name', 'middle_name', 'phone']
    ordering = ['last_name', 'first_name']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('club', 'last_name', 'first_name', 'middle_name', 'birth_date')
        }),
        ('Контактная информация', {
            'fields': ('city', 'address', 'phone', 'workplace')
        }),
        ('Информация о занятиях', {
            'fields': ('start_date', 'current_level', 'last_attestation_date')
        }),
    )
    
    inlines = [AttestationInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        # Если пользователь - администратор клуба, показываем только его студентов
        try:
            user_clubs = Club.objects.filter(admins__user=request.user)
            return qs.filter(club__in=user_clubs)
        except:
            return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "club":
            if not request.user.is_superuser:
                try:
                    user_clubs = Club.objects.filter(admins__user=request.user)
                    kwargs["queryset"] = user_clubs
                    if user_clubs.count() == 1:
                        kwargs["initial"] = user_clubs.first()
                except:
                    kwargs["queryset"] = Club.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        
        if obj is None:
            return True
        
        try:
            user_clubs = Club.objects.filter(admins__user=request.user)
            return obj.club in user_clubs
        except:
            return False


@admin.register(Attestation)
class AttestationAdmin(admin.ModelAdmin):
    list_display = ['student', 'level', 'date', 'city']
    list_filter = ['level', 'date', 'city', 'student__club']
    search_fields = ['student__last_name', 'student__first_name', 'city']
    ordering = ['-date']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        # Если пользователь - администратор клуба, показываем только аттестации его студентов
        try:
            user_clubs = Club.objects.filter(admins__user=request.user)
            return qs.filter(student__club__in=user_clubs)
        except:
            return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            if not request.user.is_superuser:
                try:
                    user_clubs = Club.objects.filter(admins__user=request.user)
                    kwargs["queryset"] = Student.objects.filter(club__in=user_clubs)
                except:
                    kwargs["queryset"] = Student.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ClubAdmin)
class ClubAdminModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'club']
    list_filter = ['club']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'club__name']
    
    def has_module_permission(self, request):
        # Только суперпользователи могут управлять администраторами клубов
        return request.user.is_superuser
