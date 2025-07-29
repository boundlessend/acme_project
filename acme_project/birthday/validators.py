from datetime import date

from django.core.exceptions import ValidationError


def real_age(value: date) -> None:
    today = date.today()
    # Считаем полный возраст в годах
    age = today.year - value.year
    # Если день рождения в этом году ещё не наступил — уменьшаем возраст на 1
    if (today.month, today.day) < (value.month, value.day):
        age -= 1

    if age < 1 or age > 120:
        raise ValidationError(
            'Ожидается возраст от 1 года до 120 лет'
        )
