from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='home'),
    
    # Órdenes
    path('ordenes/', views.orden_list, name='orden_list'),
    path('ordenes/nueva/', views.orden_create, name='orden_create'),
    path('ordenes/<int:pk>/', views.orden_detail, name='orden_detail'),
    path('ordenes/<int:pk>/editar/', views.orden_edit, name='orden_edit'),
    path('ordenes/<int:pk>/cambiar-estado/', views.cambiar_estado_orden, name='cambiar_estado_orden'),
    path('ordenes/<int:pk>/asignar-repartidor/', views.asignar_repartidor, name='asignar_repartidor'),
    
    # Despachos
    path('despachos/', views.despacho_list, name='despacho_list'),
    path('despachos/<int:pk>/', views.despacho_detail, name='despacho_detail'),
    path('ordenes/<int:orden_id>/despacho/nuevo/', views.despacho_create, name='despacho_create'),
    
    # Motos
    path('motos/', views.moto_list, name='moto_list'),
    path('motos/nueva/', views.moto_create, name='moto_create'),
    path('motos/<int:pk>/', views.moto_detail, name='moto_detail'),
    path('motos/<int:pk>/editar/', views.moto_edit, name='moto_edit'),
    path('motos/<int:moto_id>/asignar/', views.asignar_moto_repartidor, name='asignar_moto_repartidor'),
    
    # Reportes
    path('reportes/', views.reporte_list, name='reporte_list'),
    path('reportes/<int:pk>/export-csv/', views.reporte_export_csv, name='reporte_export_csv'),
    
    # Usuarios
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/nuevo/', views.usuario_create, name='usuario_create'),
    path('usuarios/<int:pk>/', views.usuario_detail, name='usuario_detail'),
    path('usuarios/<int:pk>/editar/', views.usuario_edit, name='usuario_edit'),
    path('usuarios/<int:pk>/cambiar-estado-turno/', views.cambiar_estado_turno, name='cambiar_estado_turno'),
]

