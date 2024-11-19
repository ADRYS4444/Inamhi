from rest_framework import serializers
from .models import Programmers
from django import forms

class ProgrammersForm(forms.ModelForm):
    class Meta:
        model = Programmers
        fields = '__all__'

class ProgrammerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programmers
        fields = '__all__'

    def validate_telefono_institucional(self, value):
        if not value.isdigit() or len(value) not in [9, 10, 11, 15]:
            raise serializers.ValidationError("El teléfono institucional debe ser un número válido de 9, 10, 11 o 15 dígitos.")
        return value

    def validate_extension_telefonica(self, value):
        if not value.isdigit() or len(value) > 5:
            raise serializers.ValidationError("La extensión telefónica debe ser un número válido de hasta 5 dígitos.")
        return value
