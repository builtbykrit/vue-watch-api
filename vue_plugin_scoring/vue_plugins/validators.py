from django.core.exceptions import ValidationError


def validate_zero_or_greater(value):
    if value < 0:
        raise ValidationError(_('%(value) is not greater than or equal to 0'), params={'value': value})


def validate_one_or_less(value):
    if value < 0:
        raise ValidationError(_('%(value) is not less than or equal to 1'), params={'value': value})
