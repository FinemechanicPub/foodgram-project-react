from rest_framework import serializers


class NotEqualValidator:
    """Validator to test the values in fields are not equal."""

    message = 'Fields must not be equal'

    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message or self.message

    def __call__(self, attrs):
        unique_values = set(
            value for field, value in attrs.items() if field in self.fields
        )
        if len(unique_values) != len(self.fields):
            raise serializers.ValidationError(self.message)
