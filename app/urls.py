from django.urls import path
from . import views
from .views import buscar_chofer_nombre_view, login_view, logout_view, loginChoferes_view, registroViajes, agregar_provincias
from .views import eliminar_viaje, eliminar_chofer, eliminar_vehiculo
from .views import reservar_salas, eliminar_reserva
from django.views.generic import TemplateView
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('home')),
    path('home/', views.home, name='home'),
    path('list_programmers/', views.list_programmers, name='list_programmers'),
    path('create_programmer/', views.CreateProgrammerView.as_view(), name='create_programmer'),
    path('update_programmer/<int:id>/', views.UpdateProgrammerView.as_view(), name='update_programmer'),
    path('delete_programmer/<int:pk>/', views.DeleteProgrammerView.as_view(), name='delete_programmer'),
    path('login/', login_view, name='login'),  
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),
    path('vista/', TemplateView.as_view(template_name='vista.html'), name='vista'),
    path('logout/', logout_view, name='logout'),
    path('loginChoferes/', loginChoferes_view, name='loginChoferes'),
    path('registroViajes/', registroViajes, name='registroViajes'),
    path('eliminar_viaje/<int:viaje_id>/', eliminar_viaje, name='eliminar_viaje'),
    path('agregar-provincias/', agregar_provincias, name='agregar_provincias'),
    path('choferes/', views.lista_choferes_view, name='lista_choferes'),
    path('agregar_chofer/', views.agregar_chofer_view, name='agregar_chofer'),
    path('buscar_chofer/', views.buscar_chofer_view, name='buscar_chofer'),
    path('buscar_chofer_nombre/', buscar_chofer_nombre_view, name='buscar_chofer_nombre'),
    path('agregar_vehiculo/', views.agregar_vehiculo_view, name='agregar_vehiculo'),
    path('eliminar_chofer/<int:chofer_id>/', eliminar_chofer, name='eliminar_chofer'),  
    path('eliminar_vehiculo/<int:vehiculo_id>/', eliminar_vehiculo, name='eliminar_vehiculo'),
    path('viajes_choferes/', views.viajes_choferes, name='viajes_choferes'),
    path('choferes/<int:chofer_id>/viajes/', views.viajes_calendario, name='viajes_calendario'),
    path('reservar_salas/', reservar_salas, name='reservar_salas'),
    path('eliminar_reserva/<int:reserva_id>/', eliminar_reserva, name='eliminar_reserva'),
    path('reservas/', views.reservas_view, name='reservas'),
    path('loginSalas/', views.loginSalas_view, name='loginSalas'),
    path('vista-reservas/', views.vista_reservas_view, name='vista_reservas'),
    path('enviar-formulario/', views.enviar_formulario, name='enviar_formulario'),
]
