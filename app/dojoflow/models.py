from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Club(models.Model):
    """Модель клуба Айкидо"""
    name = models.CharField(max_length=200, verbose_name="Название клуба")
    city = models.CharField(max_length=100, verbose_name="Город")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Клуб"
        verbose_name_plural = "Клубы"
        ordering = ['city', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.city})"


class AttestationLevel(models.Model):
    """Модель уровня аттестации"""
    LEVEL_CHOICES = [
        ('10ky', '10 кю'),
        ('9ky', '9 кю'),
        ('8ky', '8 кю'),
        ('7ky', '7 кю'),
        ('6ky', '6 кю'),
        ('5ky', '5 кю'),
        ('4ky', '4 кю'),
        ('3ky', '3 кю'),
        ('2ky', '2 кю'),
        ('1ky', '1 кю'),
        ('1dan', '1 дан'),
        ('2dan', '2 дан'),
        ('3dan', '3 дан'),
        ('4dan', '4 дан'),
        ('5dan', '5 дан'),
        ('6dan', '6 дан'),
        ('7dan', '7 дан'),
    ]
    
    level = models.CharField(
        max_length=5, 
        choices=LEVEL_CHOICES, 
        unique=True,
        verbose_name="Уровень"
    )
    order = models.PositiveIntegerField(
        unique=True,
        verbose_name="Порядок",
        help_text="Порядковый номер для сортировки (1 - самый низкий, 17 - самый высокий)"
    )
    
    class Meta:
        verbose_name = "Уровень аттестации"
        verbose_name_plural = "Уровни аттестации"
        ordering = ['order']
    
    def __str__(self):
        return self.get_level_display()


class Student(models.Model):
    """Модель занимающегося"""
    club = models.ForeignKey(
        Club, 
        on_delete=models.PROTECT,
        verbose_name="Клуб",
        related_name="students"
    )
    
    # Персональная информация
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    birth_date = models.DateField(verbose_name="Дата рождения")
    
    # Контактная информация
    city = models.CharField(max_length=100, verbose_name="Город")
    address = models.TextField(verbose_name="Адрес")
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
    )
    phone = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        verbose_name="Телефон"
    )
    
    # Дополнительная информация
    workplace = models.CharField(max_length=200, blank=True, verbose_name="Место работы")
    
    # Информация о занятиях
    start_date = models.DateField(verbose_name="Дата начала занятий")
    
    # Участие в аттестациях
    attestations = models.ManyToManyField(
        'Attestation',
        blank=True,
        verbose_name="Участие в аттестациях",
        related_name="participants"
    )
    
    # Системные поля
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления записи")
    
    class Meta:
        verbose_name = "Занимающийся"
        verbose_name_plural = "Занимающиеся"
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()
    
    @property
    def full_name(self):
        """Полное имя"""
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()
    
    @property
    def current_level(self):
        """Текущий уровень (из последней аттестации)"""
        latest_student_attestation = self.student_attestations.select_related('level').order_by('-attestation__date').first()
        return latest_student_attestation.level if latest_student_attestation else None
    
    @property
    def last_attestation_date(self):
        """Дата последней аттестации (вычисляется автоматически)"""
        latest_student_attestation = self.student_attestations.select_related('attestation').order_by('-attestation__date').first()
        return latest_student_attestation.attestation.date if latest_student_attestation else None
    
    @property
    def attestation_history(self):
        """История аттестаций студента"""
        return self.student_attestations.select_related('attestation', 'level').order_by('-attestation__date')


class Attestation(models.Model):
    """Модель аттестации - мероприятие/событие"""
    date = models.DateField(verbose_name="Дата аттестации")
    city = models.CharField(max_length=100, verbose_name="Место проведения (город)")
    
    # Системные поля
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    
    class Meta:
        verbose_name = "Аттестация"
        verbose_name_plural = "Аттестации"
        ordering = ['-date']
        unique_together = ['date', 'city']  # Одна аттестация в день в одном городе
    
    def __str__(self):
        return f"Аттестация {self.date} ({self.city})"


class StudentAttestation(models.Model):
    """Промежуточная модель для связи студент-аттестация с указанием полученного уровня"""
    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        verbose_name="Студент",
        related_name="student_attestations"
    )
    attestation = models.ForeignKey(
        Attestation,
        on_delete=models.CASCADE,
        verbose_name="Аттестация",
        related_name="student_attestations"
    )
    level = models.ForeignKey(
        AttestationLevel,
        on_delete=models.PROTECT,
        verbose_name="Полученный уровень",
        related_name="student_attestations"
    )
    
    # Системные поля
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    
    class Meta:
        verbose_name = "Участие в аттестации"
        verbose_name_plural = "Участия в аттестациях"
        unique_together = ['student', 'attestation']  # Студент может участвовать в аттестации только один раз
        ordering = ['-attestation__date']
    
    def __str__(self):
        return f"{self.student} - {self.attestation} ({self.level})"


class ClubAdmin(models.Model):
    """Модель администратора клуба"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="club_admins"
    )
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        verbose_name="Клуб",
        related_name="admins"
    )
    
    class Meta:
        verbose_name = "Администратор клуба"
        verbose_name_plural = "Администраторы клубов"
        unique_together = ['user', 'club']  # Один пользователь не может быть дважды администратором одного клуба
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.club}"
