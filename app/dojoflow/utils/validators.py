"""
Кастомные валидаторы
"""
import re
from datetime import date
from django.core.exceptions import ValidationError


def validate_phone_number(value: str) -> None:
    """
    Валидатор для номера телефона
    """
    if not value:
        return
    
    # Убираем все нецифровые символы кроме +
    cleaned = re.sub(r'[^\d+]', '', value)
    
    # Проверяем формат
    if not re.match(r'^\+?\d{10,15}$', cleaned):
        raise ValidationError(
            'Номер телефона должен содержать от 10 до 15 цифр и может начинаться с +'
        )


def validate_date_not_future(value: date) -> None:
    """
    Валидатор, проверяющий что дата не в будущем
    """
    if value and value > date.today():
        raise ValidationError('Дата не может быть в будущем')


def validate_birth_date(value: date) -> None:
    """
    Валидатор для даты рождения
    """
    validate_date_not_future(value)
    
    if value:
        # Проверяем, что возраст не больше 150 лет
        age = date.today().year - value.year
        if age > 150:
            raise ValidationError('Дата рождения не может быть более 150 лет назад')
        
        # Проверяем, что возраст не меньше 3 лет (минимальный возраст для айкидо)
        if age < 3:
            raise ValidationError('Минимальный возраст для занятий айкидо - 3 года') 