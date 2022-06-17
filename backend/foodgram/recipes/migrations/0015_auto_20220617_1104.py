# Generated by Django 2.2 on 2022-06-17 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_auto_20220617_0024'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='no duplicated ingredient in recipe'),
        ),
    ]