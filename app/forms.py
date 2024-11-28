from django import forms
from .models import Chofer, Vehiculo


class ChoferForm(forms.ModelForm):
    class Meta:
        model = Chofer
        fields = ['nombre', 'cedula']


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa']

from .models import Viaje

VIATICOS_CHOICES = [
    ('con_viaticos', 'Con Viáticos'),
    ('sin_viaticos', 'Sin Viáticos'),
]

class ViajeForm(forms.ModelForm):
    viaticos = forms.ChoiceField(choices=VIATICOS_CHOICES) 

    class Meta:
        model = Viaje
        fields = ['viaticos', 'chofer', 'vehiculo', 'fecha_salida', 'hora_salida', 'fecha_llegada', 'hora_llegada', 'direccion', 'provincia']
