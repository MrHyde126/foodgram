import re

from django.core.exceptions import ValidationError


def check_login(login):
    if login.lower() == 'me':
        raise ValidationError('Логин `me` зарезервирован системой!')
    if re.match(r'^[\w.@+-]+\Z', login) is None:
        raise ValidationError('Логин содержит недопустимые символы!')
    return login
