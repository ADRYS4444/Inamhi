#AGENDA TELEFONICA
from django.db import models

class Programmers(models.Model):
    apellidos_y_nombres = models.CharField(max_length=100)
    puesto_institucional = models.CharField(max_length=100)
    unidad_perteneciente = models.CharField(max_length=100)
    direccion_institucional = models.CharField(max_length=200)
    ciudad_laboral = models.CharField(max_length=100)
    telefono_institucional = models.CharField(max_length=15)
    extension_telefonica = models.CharField(max_length=5, default='00000')
    correo_institucional = models.EmailField()

    def __str__(self):
        return self.apellidos_y_nombres

    class Meta:
        verbose_name = "Programador"
        verbose_name_plural = "Programadores"

#AGENDA DE VIAJES
from django.db import models
from django.utils import timezone

class Chofer(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True, null=True) 

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"
    
    def esta_de_viaje(self):
        viajes = Viaje.objects.filter(chofer=self)

        for viaje in viajes:
            print(f"Evaluando viaje: {viaje}")  

            if viaje.fecha_llegada is None and viaje.fecha_salida <= timezone.now():
                print(f"{self.nombre} está de viaje.")
                return True  

            elif viaje.fecha_salida > timezone.now():
                print(f"{self.nombre} no está de viaje, el viaje es en el futuro.")  
                return False

        return False


class Vehiculo(models.Model):
    placa = models.CharField(max_length=10)

class Provincia(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Viaje(models.Model):
    chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_salida = models.DateTimeField()
    hora_salida = models.TimeField(null=True, blank=True)
    fecha_llegada = models.DateTimeField(null=True, blank=True) 
    hora_llegada = models.TimeField(null=True, blank=True)
    direccion = models.CharField(max_length=255)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    viaticos = models.CharField(max_length=20, choices=[('con_viaticos', 'Con Viáticos'), ('sin_viaticos', 'Sin Viáticos')], default='sin_viaticos')

    def duracion_viaje(self):
        if self.fecha_llegada:
            return (self.fecha_llegada - self.fecha_salida).days
        else:
            return None  

    def __str__(self):
        return f"Viaje de {self.chofer} a {self.provincia}"




#AGENDA DE RESERVAS
from django.db import models

class Sala(models.Model):
    nombre = models.CharField(max_length=100)

class Reserva(models.Model):
    nombre_reservante = models.CharField(max_length=100)
    fecha = models.DateField()
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ('fecha', 'sala', 'hora_inicio', 'hora_fin')

    def __str__(self):
        return f"{self.nombre_reservante} - {self.fecha} - {self.sala.nombre}"
