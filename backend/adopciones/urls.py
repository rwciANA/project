from django.urls import path
from . import views

app_name = 'adopciones'

urlpatterns = [
     path(
        "api/veterinarios/",
        views.api_veterinarios,
        name="api_veterinarios"
    ),
    # ==================== ANIMALES ====================
    path('', views.animal_list, name='animal_list'),
    path('<int:pk>/', views.animal_detail, name='animal_detail'),
    path('crear/', views.animal_create, name='animal_create'),
    path('<int:pk>/editar/', views.animal_update, name='animal_update'),
    path('<int:pk>/borrar/', views.animal_delete, name='animal_delete'),

    # ==================== CITAS ====================
    path('citas/', views.cita_list, name='cita_list'),
    path('citas/nueva/', views.cita_create, name='cita_create'),
    path('citas/<int:pk>/editar/', views.cita_update, name='cita_update'),
    path('citas/<int:pk>/borrar/', views.cita_delete, name='cita_delete'),

    # ==================== VACUNAS ====================
    path('vacunas/', views.vacuna_list, name='vacuna_list'),
    path('vacunas/nueva/', views.vacuna_create, name='vacuna_create'),
    path('vacunas/<int:pk>/editar/', views.vacuna_update, name='vacuna_update'),
    path('vacunas/<int:pk>/borrar/', views.vacuna_delete, name='vacuna_delete'),

    # ==================== PANEL VETERINARIO ====================
    path('alertas/', views.panel_alertas, name='panel_alertas'),
    path('registro-paciente/', views.registro_paciente, name='registro_paciente'),
    path('<int:pk>/adoptar/', views.solicitud_adopcion, name='solicitud_adopcion'),
    path('casos-exito/', views.casos_exito, name='casos_exito'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # ==================== APIs JSON ====================
    path('api/', views.animal_api, name='animal_api'),
    path('api/citas/', views.api_citas, name='api_citas'),
    path('api/vacunas/', views.api_vacunas, name='api_vacunas'),
    path('api/mis-mascotas/', views.api_mis_mascotas, name='api_mis_mascotas'),
    path('api/adopciones/solicitud/', views.api_solicitud_adopcion, name='api_solicitud_adopcion'),

    # ==================== AUTENTICACION ====================
    path('api/login/', views.api_login, name='api_login'),
    path('api/registro/', views.api_registro, name='api_registro'),
    path('api/logout/', views.api_logout, name='api_logout'),
    
]