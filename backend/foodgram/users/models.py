from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import username_validator


class WebUser(AbstractUser):
    username = models.CharField(
        'имя пользователя',
        max_length=150,
        unique=True,
        validators=(username_validator(),)
    )
    email = models.EmailField('электронная почта', max_length=254, unique=True)
    first_name = models.CharField(
        'имя',
        max_length=150,
        null=True, blank=False
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        null=True, blank=False
    )


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        WebUser,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    author = models.ForeignKey(
        WebUser,
        on_delete=models.CASCADE,
        related_name='authors'
    )

    def __str__(self) -> str:
        return f'{self.subscriber} подписан на {self.author}'
