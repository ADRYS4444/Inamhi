from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Programmers
from .serializers import ProgrammerSerializer
from django.shortcuts import render, get_object_or_404
from django.views import View


import json

class UpdateProgrammerView(View):
    def put(self, request, id):
        data = json.loads(request.body)
        programmer = get_object_or_404(Programmers, id=id)
        
        programmer.apellidos_y_nombres = data['apellidos_y_nombres']
        programmer.puesto_institucional = data['puesto_institucional']
        programmer.unidad_perteneciente = data['unidad_perteneciente']
        programmer.direccion_institucional = data['direccion_institucional']
        programmer.ciudad_laboral = data['ciudad_laboral']
        programmer.telefono_institucional = data['telefono_institucional']
        programmer.extension_telefonica = data['extension_telefonica']
        programmer.correo_institucional = data['correo_institucional']
        programmer.save()

        return JsonResponse({'message': 'Programador actualizado correctamente!'})

    def dispatch(self, request, *args, **kwargs):
        if request.method != 'PUT':
            return JsonResponse({'error': 'Método no permitido'}, status=405)
        return super().dispatch(request, *args, **kwargs)




from django.views import View
import json

class CreateProgrammerView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            programmer = Programmers.objects.create(
                apellidos_y_nombres=data['apellidos_y_nombres'],
                puesto_institucional=data['puesto_institucional'],
                unidad_perteneciente=data['unidad_perteneciente'],
                direccion_institucional=data['direccion_institucional'],
                ciudad_laboral=data['ciudad_laboral'],
                telefono_institucional=data['telefono_institucional'],
                extension_telefonica=data['extension_telefonica'],
                correo_institucional=data['correo_institucional'],
            )
            return JsonResponse({'message': 'Programador creado correctamente.', 'id': programmer.id}, status=201)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)





class DeleteProgrammerView(View):
    def delete(self, request, pk):
        try:
            programmer = Programmers.objects.get(pk=pk)
            programmer.delete()
            return JsonResponse({'message': 'Programador eliminado correctamente.'}, status=204)
        except Programmers.DoesNotExist:
            return JsonResponse({'message': 'Programador no encontrado.'}, status=404)

def list_programmers(request):
    programmers = Programmers.objects.all().values()  
    return JsonResponse({'programmers': programmers})




def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def list_programmers(request):
    programmers = Programmers.objects.all()
    serializer = ProgrammerSerializer(programmers, many=True)
    return Response({'programmers': serializer.data})

@api_view(['GET'])
def get_programmer(request, pk):
    try:
        programmer = Programmers.objects.get(pk=pk)
        serializer = ProgrammerSerializer(programmer)
        return Response(serializer.data)
    except Programmers.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_programmer(request):
    serializer = ProgrammerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def update_programmer(request, pk):
    try:
        programmer = Programmers.objects.get(pk=pk)
    except Programmers.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProgrammerSerializer(programmer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('index')  
            else:
                return redirect('vista')  
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})

    return render(request, 'login.html')

    



from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login') 

def home(request):
    return render(request, 'home.html')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages


#VIAJES
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def loginChoferes_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('registroViajes')  
            else:
                return redirect('buscar_chofer_nombre')  
        else:
            return render(request, 'loginChoferes.html', {'error': 'Credenciales inválidas'})

    return render(request, 'loginChoferes.html')


from .models import Viaje, Chofer, Vehiculo, Provincia
from django.http import HttpResponse

from django.db.models.functions import ExtractMonth, ExtractYear
from datetime import timedelta


from django.db.models import FloatField, ExpressionWrapper, F, Sum, Func

class MonthName(Func):
    """Clase personalizada para convertir un número de mes en nombre del mes."""
    function = 'TO_CHAR'
    template = "TO_CHAR(%(expressions)s, 'Month')"

import calendar 
from django.utils import timezone

def registroViajes(request):
    choferes = Chofer.objects.all()
    vehiculos = Vehiculo.objects.all()
    provincias = Provincia.objects.all()
    registros = Viaje.objects.all().select_related('provincia')

    for viaje in registros:
        if viaje.fecha_llegada: 
            viaje.duracion_viaje = (viaje.fecha_llegada - viaje.fecha_salida).days
        else:
            viaje.duracion_viaje = 'No disponible'

    chofer_id = request.GET.get('chofer_id')
    meses_viajes = []

    if chofer_id:
        viajes = (
            Viaje.objects
            .filter(chofer_id=chofer_id)
            .annotate(mes=ExtractMonth('fecha_salida'), anio=ExtractYear('fecha_salida'))
            .annotate(
                duracion_viaje=ExpressionWrapper(
                    (F('fecha_llegada') - F('fecha_salida')) / timedelta(days=1),
                    output_field=FloatField()
                )
            )
            .values('mes', 'anio')
            .annotate(total_dias_viaje=Sum('duracion_viaje'))
            .order_by('anio', 'mes')
        )

        for viaje in viajes:
            mes_nombre = calendar.month_name[viaje['mes']]
            meses_viajes.append({
                'mes': mes_nombre,
                'anio': viaje['anio'],
                'total_dias_viaje': viaje['total_dias_viaje']
            })

    if request.method == 'POST':
        chofer_id = request.POST['chofer']
        vehiculo_id = request.POST['vehiculo']
        fecha_salida = request.POST['fecha_salida']
        hora_salida = request.POST['hora_salida']
        fecha_llegada = request.POST['fecha_llegada']
        hora_llegada = request.POST['hora_llegada']
        direccion = request.POST['direccion']
        provincia_id = request.POST['provincia']
        viaticos = request.POST.get('viaticos', 'sin_viaticos')  # Asegúrate de obtener el valor

        fecha_hora_salida = timezone.datetime.strptime(f"{fecha_salida} {hora_salida}", '%Y-%m-%d %H:%M')
        fecha_hora_llegada = timezone.datetime.strptime(f"{fecha_llegada} {hora_llegada}", '%Y-%m-%d %H:%M')

        viajes_superpuestos = Viaje.objects.filter(
            chofer_id=chofer_id,
            fecha_salida__lt=fecha_hora_llegada,
            fecha_llegada__gt=fecha_hora_salida
        )

        viaje_superpuesto = Viaje.objects.filter(
            vehiculo_id=vehiculo_id,
            fecha_salida__lt=fecha_hora_llegada,
            fecha_llegada__gt=fecha_hora_salida
        )

        if viajes_superpuestos.exists():
            messages.error(request, 'El chofer ya tiene un viaje registrado en este rango de tiempo.')
            return redirect('registroViajes')

        if viaje_superpuesto.exists():
            messages.error(request, 'El vehiculo ya tiene un viaje registrado en este rango de tiempo.')
            return redirect('registroViajes')

        viaje = Viaje(
            chofer_id=chofer_id,
            vehiculo_id=vehiculo_id,
            fecha_salida=fecha_hora_salida,
            hora_salida=hora_salida,
            fecha_llegada=fecha_hora_llegada,
            hora_llegada=hora_llegada,
            direccion=direccion,
            provincia_id=provincia_id,
            viaticos=viaticos  # Guardar los viáticos correctamente
        )
        viaje.save()
        messages.success(request, 'Viaje registrado exitosamente.')
        return redirect('registroViajes')

    return render(request, 'registroViajes.html', {
        'choferes': choferes,
        'vehiculos': vehiculos,
        'provincias': provincias,
        'registros': registros,
        'meses_viajes': meses_viajes,
        'chofer_id': chofer_id,
    })


from django.db.models import fields

def viajes_choferes(request):
    choferes = Chofer.objects.all() 
    meses_viajes = []
    chofer_id = request.GET.get('chofer_id')

    if chofer_id:
        viajes = (
            Viaje.objects
            .filter(chofer_id=chofer_id)
            .select_related('provincia')  
            .annotate(
                mes=ExtractMonth('fecha_salida'), 
                anio=ExtractYear('fecha_salida'),
                duracion_viaje=ExpressionWrapper(
                    F('fecha_llegada') - F('fecha_salida'),
                    output_field=fields.DurationField()
                )
            )
            .annotate(duracion_en_dias=ExpressionWrapper(
                F('duracion_viaje') / timedelta(days=1),
                output_field=fields.FloatField()
            ))
            .values('mes', 'anio', 'provincia__nombre')  
            .annotate(total_dias_viaje=Sum('duracion_en_dias'))
            .order_by('anio', 'mes')
        )

        for viaje in viajes:
            mes_nombre = calendar.month_name[viaje['mes']]
            meses_viajes.append({
                'mes': mes_nombre,
                'anio': viaje['anio'],
                'provincia': viaje['provincia__nombre'],  
                'total_dias_viaje': viaje['total_dias_viaje']
            })

    return render(request, 'viajes_choferes.html', {
        'choferes': choferes,
        'meses_viajes': meses_viajes,
        'chofer_id': chofer_id,
    })


def viajes_chofer(request, chofer_id):
    chofer_viajes = Viaje.objects.filter(chofer_id=chofer_id)
    
    eventos = []
    for viaje in chofer_viajes:
        eventos.append({
            'title': f'Viaje a {viaje.provincia}',
            'start': viaje.fecha_inicio.isoformat(),
            'end': viaje.fecha_fin.isoformat(),
            'allDay': True,  
            'color': 'red'  
        })

    context = {
        'chofer_id': chofer_id,
        'eventos_json': json.dumps(eventos) 
    }
    return render(request, 'viajes_calendario.html', context)


from datetime import datetime

def viajes_calendario(request, chofer_id):
    chofer = get_object_or_404(Chofer, id=chofer_id)
    viajes = Viaje.objects.filter(chofer=chofer)

    evento = []
    for viaje in viajes:
        start_datetime = viaje.fecha_salida.isoformat()
        if viaje.hora_salida:
            start_datetime = f"{start_datetime}T{viaje.hora_salida}"

        end_datetime = viaje.fecha_llegada.isoformat()
        if viaje.hora_llegada:
            end_datetime = f"{end_datetime}T{viaje.hora_llegada}"

        start_datetime = start_datetime[:-6] if start_datetime[-6:] == '+00:00' else start_datetime
        end_datetime = end_datetime[:-6] if end_datetime[-6:] == '+00:00' else end_datetime

        evento.append({
            'title': f'Viaje a {viaje.provincia.nombre}',  
            'start': start_datetime,  
            'end': end_datetime,  
            'allDay': False,  
            'color': 'red' 
        })

    evento_json = json.dumps(evento)

    return render(request, 'viajes_calendario.html', {
        'chofer': chofer,
        'evento_json': evento_json
    })



def agregar_provincias(request):
    provincias = [
        "Azuay", "Bolívar", "Cañar", "Carchi", "Chimborazo",
        "Cotopaxi", "El Oro", "Esmeraldas", "Galápagos", "Guayas",
        "Imbabura", "Loja", "Los Ríos", "Manabí", "Morona Santiago",
        "Napo", "Pastaza", "Pichincha", "Santa Elena", "Santo Domingo de los Tsáchilas",
        "Sucumbíos", "Tungurahua", "Zamora-Chinchipe"
    ]

    for provincia in provincias:
        Provincia.objects.get_or_create(nombre=provincia)

    return HttpResponse("Provincias agregadas.")


def eliminar_viaje(request, viaje_id):
    try:
        viaje = Viaje.objects.get(id=viaje_id)
        viaje.delete()
    except Viaje.DoesNotExist:
        
        pass
    return redirect('registroViajes') 

from .forms import ChoferForm, VehiculoForm


from django.urls import reverse

def lista_choferes_view(request):
    choferes = Chofer.objects.all()  
    return render(request, 'lista_choferes.html', {'choferes': choferes})

from .forms import ChoferForm

def agregar_chofer_view(request):
    if request.method == 'POST':
        form = ChoferForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('agregar_chofer')  
    else:
        form = ChoferForm()

    choferes = Chofer.objects.all()  
    return render(request, 'agregar_chofer.html', {'form': form, 'choferes': choferes})


from django.utils import timezone

def buscar_chofer_view(request):
    choferes_data = []

    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        choferes = Chofer.objects.filter(cedula=cedula)

        for chofer in choferes:
            viajes_data = []

            for viaje in chofer.viaje_set.all():
                viajes_data.append({
                    'origen': viaje.provincia.nombre,
                    'duracion': viaje.duracion_viaje() if viaje.fecha_llegada else 'No disponible',
                    'fecha_salida': viaje.fecha_salida,
                    'hora_salida': viaje.hora_salida,
                    'fecha_llegada': viaje.fecha_llegada,
                    'hora_llegada': viaje.hora_llegada,
                    'viaticos': viaje.viaticos,  # Agregamos los viáticos aquí
                })

            choferes_data.append({
                'nombre': chofer.nombre,
                'cedula': chofer.cedula,
                'viajes': viajes_data,
            })

    return render(request, 'buscar_chofer.html', {
        'choferes': choferes_data
    })


def buscar_chofer_nombre_view(request):
    choferes_data = []

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        choferes = Chofer.objects.filter(nombre__icontains=nombre) 

        for chofer in choferes:
            viajes_data = []

            for viaje in chofer.viaje_set.all():
                viajes_data.append({
                    'origen': viaje.provincia.nombre,
                    'duracion': viaje.duracion_viaje() if viaje.fecha_llegada else 'No disponible',
                    'fecha_salida': viaje.fecha_salida,
                    'hora_salida': viaje.hora_salida,
                    'fecha_llegada': viaje.fecha_llegada,
                    'hora_llegada': viaje.hora_llegada,
                    'viaticos': viaje.viaticos,  # Agregamos los viáticos aquí
                })

            choferes_data.append({
                'nombre': chofer.nombre,
                'cedula': chofer.cedula,
                'viajes': viajes_data,
            })

    return render(request, 'buscar_chofer_nombre.html', {
        'choferes': choferes_data
    })




def agregar_vehiculo_view(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('registroViajes') 
    else:
        form = VehiculoForm()

    vehiculos = Vehiculo.objects.all() 
    return render(request, 'agregar_vehiculo.html', {'form': form, 'vehiculos': vehiculos})


from django.shortcuts import redirect, get_object_or_404

def eliminar_chofer(request, chofer_id):
    chofer = get_object_or_404(Chofer, id=chofer_id)
    chofer.delete()
    return redirect('agregar_chofer')  

def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    vehiculo.delete()
    return redirect('agregar_vehiculo') 



#RESERVAS
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Reserva, Sala
from datetime import datetime

def reservar_salas(request):
    if request.method == 'POST':
        nombre_reservante = request.POST['nombre']
        fecha = request.POST['fecha']
        sala_id = request.POST['sala']
        hora_inicio = request.POST['hora_inicio']
        hora_fin = request.POST['hora_fin']

        conflicto = Reserva.objects.filter(
            fecha=fecha,
            sala_id=sala_id,
            hora_inicio__lt=hora_fin,
            hora_fin__gt=hora_inicio
        ).exists()

        if conflicto:
            messages.error(request, '¡Ya existe una reserva para esa sala en ese horario!')
            return redirect('reservar_salas')

        nueva_reserva = Reserva(
            nombre_reservante=nombre_reservante,
            fecha=fecha,
            sala_id=sala_id,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )

        try:
            nueva_reserva.save()
            messages.success(request, 'Reserva creada exitosamente.')
            return redirect('reservar_salas')
        except IntegrityError:
            messages.error(request, 'Ocurrió un error al guardar la reserva.')

    salas = Sala.objects.all()
    reservas = Reserva.objects.all()

    ocupadas = {}
    for reserva in reservas:
        if reserva.fecha not in ocupadas:
            ocupadas[reserva.fecha] = {}
        if reserva.sala_id not in ocupadas[reserva.fecha]:
            ocupadas[reserva.fecha][reserva.sala_id] = []
        ocupadas[reserva.fecha][reserva.sala_id].append((reserva.hora_inicio, reserva.hora_fin))

    ocupadas_transformadas = transformar_fechas(ocupadas)

    return render(request, 'reservar_salas.html', {
        'salas': salas,
        'reservas': reservas,
        'ocupadas': ocupadas_transformadas
    })

def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.delete()
    return redirect('reservar_salas')


def transformar_fechas(ocupadas):
    ocupadas_transformadas = {}
    for fecha, salas_ocupadas in ocupadas.items():
        fecha_str = fecha.strftime('%Y-%m-%d')
        ocupadas_transformadas[fecha_str] = salas_ocupadas
    return ocupadas_transformadas



import json
from .models import Reserva, Sala  

def loginSalas_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('reservar_salas') 
            else:
                return redirect('vista_reservas')  
        else:
            return render(request, 'loginSalas.html', {'error': 'Credenciales inválidas'})
    
    return render(request, 'loginSalas.html')





def reservas_view(request):
    reservas = Reserva.objects.all()
    salas = Sala.objects.all()

    ocupadas = {}
    eventos = []  

    for reserva in reservas:
        if reserva.fecha not in ocupadas:
            ocupadas[reserva.fecha] = {}
        if reserva.sala_id not in ocupadas[reserva.fecha]:
            ocupadas[reserva.fecha][reserva.sala_id] = []
        ocupadas[reserva.fecha][reserva.sala_id].append((reserva.hora_inicio, reserva.hora_fin))

        evento = {
            'title': reserva.sala.nombre,  
            'start': f'{reserva.fecha}T{reserva.hora_inicio}',  
            'end': f'{reserva.fecha}T{reserva.hora_fin}', 
            'backgroundColor': 'red',  
            'borderColor': 'red'
        }
        eventos.append(evento)

    ocupadas_transformadas = transformar_fechas(ocupadas)

    context = {
        'ocupadas': ocupadas_transformadas,
        'salas': salas,
        'eventos_json': json.dumps(eventos)  
    }

    return render(request, 'reservas.html', context)

def vista_reservas_view(request):
    reservas = Reserva.objects.all()
    salas = Sala.objects.all()

    ocupadas = {}
    eventos = []  

    for reserva in reservas:
        if reserva.fecha not in ocupadas:
            ocupadas[reserva.fecha] = {}
        if reserva.sala_id not in ocupadas[reserva.fecha]:
            ocupadas[reserva.fecha][reserva.sala_id] = []
        ocupadas[reserva.fecha][reserva.sala_id].append((reserva.hora_inicio, reserva.hora_fin))

        evento = {
            'title': reserva.sala.nombre,  
            'start': f'{reserva.fecha}T{reserva.hora_inicio}',  
            'end': f'{reserva.fecha}T{reserva.hora_fin}', 
            'backgroundColor': 'red',  
            'borderColor': 'red'
        }
        eventos.append(evento)

    ocupadas_transformadas = transformar_fechas(ocupadas)

    context = {
        'ocupadas': ocupadas_transformadas,
        'salas': salas,
        'eventos_json': json.dumps(eventos)  
    }

    return render(request, 'vista_reservas.html', context)

from django.core.mail import send_mail
from django.conf import settings

def enviar_formulario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        fecha_reserva = request.POST.get('fecha_reserva')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        sala = request.POST.get('sala')  

        asunto = f'Nuevo mensaje de {nombre} - Reserva de Sala'

        cuerpo_html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                }}
                h2 {{
                    color: #008080;
                    font-size: 24px;
                }}
                p {{
                    font-size: 16px;
                    line-height: 1.5;
                }}
                .details {{
                    background-color: #e7f7e7;
                    padding: 15px;
                    border-radius: 8px;
                }}
                .details p {{
                    margin: 5px 0;
                }}
                .highlight {{
                    color: #d9534f;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <h2>Reserva de Sala:</h2>
            <p><strong>Nombre:</strong> {nombre}</p>
            <p><strong>Correo:</strong> {correo}</p>
            <p><strong>Mensaje:</strong> {mensaje}</p>
            <div class="details">
                <p><strong>Fecha de Reserva:</strong> {fecha_reserva}</p>
                <p><strong>Hora de Inicio:</strong> {hora_inicio}</p>
                <p><strong>Hora de Fin:</strong> {hora_fin}</p>
                <p><strong>Sala Seleccionada:</strong> <span class="highlight">{sala}</span></p>
            </div>
        </body>
        </html>
        """

        try:
            send_mail(
                asunto,
                '',  
                settings.DEFAULT_FROM_EMAIL,
                ['aybanez2003@gmail.com'],
                fail_silently=False,
                html_message=cuerpo_html  
            )
            messages.success(request, 'El formulario se envió correctamente.')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al enviar el formulario: {e}')

        return redirect('vista_reservas')

    return render(request, 'vista_reservas.html')


