import datetime

from django.core.exceptions import ValidationError


def validate_year_gt_current(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            'Ошибка валидации года – год не может быть больше текущего'
        )
