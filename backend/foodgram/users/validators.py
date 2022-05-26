from django.core.validators import MaxValueValidator, RegexValidator


def username_validator():
    return RegexValidator(
        regex=r'^[\w.@+-]+$',
        message='Допускаются буквы, цифры и знаки _ @ / + - .'
    )
