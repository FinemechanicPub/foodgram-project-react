"""Дополнительные поля для сериализаторов"""
import base64

from django.core.files.base import ContentFile
from rest_framework import serializers


class DecodingImageField(serializers.ImageField):
    """Поле изображение с декодированием из Base64"""

    BASE64_SIGNATURE = ';base64,'

    def to_internal_value(self, data):
        if self.BASE64_SIGNATURE not in data:
            raise serializers.ValidationError(
                f'В данных не обнаружено "{self.BASE64_SIGNATURE}"'
            )
        headers, text = data.split(self.BASE64_SIGNATURE, 1)
        if '/' not in headers:
            raise serializers.ValidationError('Неожиданный формат запроса.')
        content_type, image_type = headers.split('/', 1)
        if content_type != 'data:image':
            raise serializers.ValidationError('Неожиданный формат запроса.')
        try:
            data = ContentFile(
                base64.b64decode(text),
                f'uploaded_file.{image_type}'
            )
        except Exception as error:
            raise serializers.ValidationError(
                f'Некорректный формат файла: {error}'
            )
        return super().to_internal_value(data)


class ImageRelatedField(serializers.SlugRelatedField):
    """Поле для преобразования поля изображения в его URL"""
    def to_representation(self, value):
        image = super().to_representation(value)
        return image.url
