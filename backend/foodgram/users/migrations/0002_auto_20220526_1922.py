# Generated by Django 2.2 on 2022-05-26 16:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='электронная почта'),
        ),
        migrations.AlterField(
            model_name='webuser',
            name='first_name',
            field=models.CharField(max_length=150, null=True, verbose_name='имя'),
        ),
        migrations.AlterField(
            model_name='webuser',
            name='last_name',
            field=models.CharField(max_length=150, null=True, verbose_name='фамилия'),
        ),
        migrations.AlterField(
            model_name='webuser',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Допускаются буквы, цифры и знаки _ @ / + - .', regex='^[\\w.@+-]+$')], verbose_name='имя пользователя'),
        ),
    ]
