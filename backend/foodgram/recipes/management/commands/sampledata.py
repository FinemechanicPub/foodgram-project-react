"""Модуль загрузки тестовых данных

Файлы csv должны в первой строке иметь названия полей модели.
Если поле является внешним ключом, то возможны два варианта:
- поле называется по шаблону {название поля}_id и содержит id в таблице
  внешнего ключа
- поле называется по шаблону {название поля} и содержит значение соответ-
  ствующего поля в таблице внешнего ключа
Во втором случае в словаре MODELS вторым компонентом значения должен быть
словарь, в котором сопоставлено имя поля модели и имя поля в модели внешнего
ключа.
Словарь MODELS содержит в качестве ключей загружаемые модели, а в качестве
занчений кортеж из имени файла .csv без расширения и словаря внешних ключей
(смотри выше).

"""
import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Model
from recipes.models import Ingredient

CSV_DIR = os.path.join(settings.BASE_DIR, 'data/')


class Command(BaseCommand):
    help = f'Loads sample data from CSV files in "{CSV_DIR}"'

    def load_csv(self, model: Model, filename: str, related={}):
        related_models = {
            field_name: (
                getattr(model, field_name).field.related_model,
                related_field_name
            )
            for field_name, related_field_name in related.items()
        }
        with open(
            os.path.join(CSV_DIR, filename),
            mode='r', encoding='utf-8', newline=''
        ) as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                params = dict(zip(headers, row))
                # Handle user model
                if hasattr(model.objects, 'create_user'):
                    model.objects.create_user(**params)
                    continue
                # Handle other types of models
                instance = model()
                # Parse every column one by one
                for key, value in params.items():
                    key_id = f'{key}_id'
                    # The column is a foreign table reference
                    if hasattr(instance, key_id):
                        # There are directions to add data to the foreign table
                        if key in related_models:
                            related_model, related_field_name = (
                                related_models[key]
                            )
                            related_object, _ = (
                                related_model.objects
                                .get_or_create(**{related_field_name: value})
                                )
                            setattr(instance, key, related_object)
                        # Foreign table should be already filled,
                        # just  add reference
                        else:
                            setattr(instance, key_id, value)
                    # The column is an ordinary data column
                    else:
                        setattr(instance, key, value)
                instance.save()

    MODELS = {
        Ingredient: ('ingredients', {'measurement_unit': 'notation'})
    }

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            for model, (filebase, related) in self.MODELS.items():
                self.load_csv(model, f'{filebase}.csv', related)
        except Exception as error:
            raise CommandError(f'что-то пошло не так. {error}')
