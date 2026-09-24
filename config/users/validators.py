from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


class PasswordValidator:

    def __call__(self, value):
        if len(value) < 8:
            raise ValidationError(_('Пароль должен быть не менее 8 символов'))
        if not re.search(r'[A-Z]', value):
            raise ValidationError(_('Пароль должен содержать хотя бы одну заглавную букву'))
        if not re.search(r'[a-z]', value):
            raise ValidationError(_('Пароль должен содержать хотя бы одну строчную букву'))
        if not re.search(r'\d', value):
            raise ValidationError(_('Пароль должен содержать хотя бы одну цифру'))


password_validator = PasswordValidator()