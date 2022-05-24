# Generated by Django 2.2 on 2022-05-24 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20220524_2303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'default_related_name': 'ingredients', 'verbose_name': 'ингредиент', 'verbose_name_plural': 'ингредиенты'},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='units',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.Unit'),
        ),
    ]