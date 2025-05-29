"""
Утилиты для работы с датами
"""
from datetime import date
from typing import Optional


def calculate_age(birth_date: Optional[date]) -> Optional[int]:
    """
    Вычисляет возраст по дате рождения
    """
    if not birth_date:
        return None
    
    today = date.today()
    return (today.year - birth_date.year - 
            ((today.month, today.day) < (birth_date.month, birth_date.day)))


def calculate_years_of_practice(start_date: Optional[date]) -> Optional[int]:
    """
    Вычисляет количество лет практики с даты начала занятий
    """
    if not start_date:
        return None
    
    today = date.today()
    years = today.year - start_date.year
    if (today.month, today.day) < (start_date.month, start_date.day):
        years -= 1
    return max(0, years) 