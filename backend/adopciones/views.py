from django.shortcuts import render, get_object_or_404, redirect
from .forms import AnimalForm, DuenoForm, SolicitudAdopcionForm
from .models import Animal, Vacuna, SolicitudAdopcion, Cita
from datetime import date, timedelta
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import Veterinario

# ==================== ANIMALES ====================
def api_veterinarios(request):
    veterinarios = Veterinario.objects.all()

    data = []

    for veterinario in veterinarios:
        data.append({
            "id": veterinario.id,
            "nombre": veterinario.nombre,
            "especialidad": veterinario.especialidad,
        })

    return JsonResponse(data, safe=False)
def animal_list(request):
    animales = Animal.objects.all()
    return render(request, 'adopciones/animal_list.html', {'animales': animales})

def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'adopciones/animal_detail.html', {'animal': animal})

def animal_delete(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        animal.delete()
        return redirect('adopciones:animal_list')
    return render(request, 'adopciones/animal_confirm_delete.html', {'animal': animal})

def animal_create(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adopciones:animal_list')
    else:
        form = AnimalForm()
    return render(request, 'adopciones/animal_form.html', {'form': form})

def animal_update(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            return redirect('adopciones:animal_list')
    else:
        form = AnimalForm(instance=animal)
    return render(request, 'adopciones/animal_form.html', {'form': form})

def animal_api(request):
    animales = Animal.objects.all()
    data = []
    for animal in animales:
        data.append({
            'id': animal.id,
            'nombre': animal.nombre,
            'especie': animal.especie,
            'raza': animal.raza,
            'edad': animal.edad,
            'descripcion': animal.descripcion,
            'estado': animal.estado,
            'foto': request.build_absolute_uri(animal.foto.url) if animal.foto else None,
        })
    return JsonResponse(data, safe=False)

# ==================== PANEL VETERINARIO  ====================

def panel_alertas(request):
    hoy = date.today()
    en_7_dias = hoy + timedelta(days=7)
    vacunas_proximas = Vacuna.objects.filter(
        proxima_dosis__gte=hoy,
        proxima_dosis__lte=en_7_dias
    ).select_related('animal')
    return render(request, 'adopciones/panel_alertas.html', {'vacunas': vacunas_proximas})

def registro_paciente(request):
    if request.method == 'POST':
        dueno_form = DuenoForm(request.POST)
        animal_form = AnimalForm(request.POST, request.FILES)
        if dueno_form.is_valid() and animal_form.is_valid():
            dueno = dueno_form.save()
            animal = animal_form.save(commit=False)
            animal.dueno = dueno
            animal.save()
            return redirect('adopciones:animal_list')
    else:
        dueno_form = DuenoForm()
        animal_form = AnimalForm()
    return render(request, 'adopciones/registro_paciente.html', {
        'dueno_form': dueno_form,
        'animal_form': animal_form
    })

def solicitud_adopcion(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        form = SolicitudAdopcionForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.animal = animal
            solicitud.save()
            return redirect('adopciones:animal_list')
    else:
        form = SolicitudAdopcionForm(initial={'animal': animal})
    return render(request, 'adopciones/solicitud_adopcion.html', {
        'form': form,
        'animal': animal
    })

def casos_exito(request):
    animales = Animal.objects.filter(estado='adoptado')
    return render(request, 'adopciones/casos_exito.html', {'animales': animales})

def dashboard(request):
    hoy = date.today()
    en_7_dias = hoy + timedelta(days=7)
    citas_hoy = Cita.objects.filter(fecha=hoy)
    vacunas_proximas = Vacuna.objects.filter(proxima_dosis__gte=hoy, proxima_dosis__lte=en_7_dias)
    solicitudes = SolicitudAdopcion.objects.order_by('-fecha_solicitud')[:5]
    animales_disponibles = Animal.objects.filter(estado='disponible').count()
    return render(request, 'adopciones/dashboard.html', {
        'citas_hoy': citas_hoy,
        'vacunas_proximas': vacunas_proximas,
        'solicitudes': solicitudes,
        'animales_disponibles': animales_disponibles,
    })

# ==================== AUTENTICACION  ====================

@csrf_exempt
def api_registro(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'El usuario ya existe'}, status=400)
        user = User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({'mensaje': 'Usuario creado correctamente', 'id': user.id}, status=201)
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'mensaje': 'Login exitoso',
                'username': user.username,
                'email': user.email,
                'es_admin': user.is_staff
            })
        else:
            return JsonResponse({'error': 'Credenciales incorrectas'}, status=401)
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

@csrf_exempt
def api_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'mensaje': 'Sesion cerrada correctamente'})
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

def es_admin(user):
    return user.is_staff

# ==================== CRUD CITAS   ====================

@login_required
@user_passes_test(es_admin)
def cita_list(request):
    citas = Cita.objects.all()
    return render(request, 'adopciones/cita_list.html', {'citas': citas})

@login_required
@user_passes_test(es_admin)
def cita_create(request):
    from .forms import CitaForm
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adopciones:cita_list')
    else:
        form = CitaForm()
    return render(request, 'adopciones/cita_form.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def cita_update(request, pk):
    from .forms import CitaForm
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            return redirect('adopciones:cita_list')
    else:
        form = CitaForm(instance=cita)
    return render(request, 'adopciones/cita_form.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def cita_delete(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        cita.delete()
        return redirect('adopciones:cita_list')
    return render(request, 'adopciones/cita_confirm_delete.html', {'cita': cita})

# ==================== CRUD VACUNAS  ====================

@login_required
@user_passes_test(es_admin)
def vacuna_list(request):
    vacunas = Vacuna.objects.all()
    return render(request, 'adopciones/vacuna_list.html', {'vacunas': vacunas})

@login_required
@user_passes_test(es_admin)
def vacuna_create(request):
    from .forms import VacunaForm
    if request.method == 'POST':
        form = VacunaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adopciones:vacuna_list')
    else:
        form = VacunaForm()
    return render(request, 'adopciones/vacuna_form.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def vacuna_update(request, pk):
    from .forms import VacunaForm
    vacuna = get_object_or_404(Vacuna, pk=pk)
    if request.method == 'POST':
        form = VacunaForm(request.POST, instance=vacuna)
        if form.is_valid():
            form.save()
            return redirect('adopciones:vacuna_list')
    else:
        form = VacunaForm(instance=vacuna)
    return render(request, 'adopciones/vacuna_form.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def vacuna_delete(request, pk):
    vacuna = get_object_or_404(Vacuna, pk=pk)
    if request.method == 'POST':
        vacuna.delete()
        return redirect('adopciones:vacuna_list')
    return render(request, 'adopciones/vacuna_confirm_delete.html', {'vacuna': vacuna})

# ==================== APIs JSON   ====================

@csrf_exempt
def api_citas(request):
    if request.method == 'GET':
        citas = Cita.objects.all()
        data = []
        for cita in citas:
            data.append({
                'id': cita.id,
                'fecha': str(cita.fecha),
                'hora': str(cita.hora),
                'motivo': cita.motivo,
                'estado': cita.estado,
                'animal': cita.animal.nombre,
                'veterinario': cita.veterinario.nombre,
            })
        return JsonResponse(data, safe=False)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'No autenticado'}, status=401)
        data = json.loads(request.body)
        from .models import Veterinario
        cita = Cita.objects.create(
            fecha=data.get('fecha'),
            hora=data.get('hora'),
            motivo=data.get('motivo'),
            animal=get_object_or_404(Animal, pk=data.get('animal_id')),
            veterinario=get_object_or_404(Veterinario, pk=data.get('veterinario_id')),
        )
        return JsonResponse({'mensaje': 'Cita creada', 'id': cita.id}, status=201)
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

@csrf_exempt
def api_vacunas(request):
    vacunas = Vacuna.objects.all()
    data = []
    for v in vacunas:
        data.append({
            'id': v.id,
            'nombre': v.nombre,
            'fecha_aplicada': str(v.fecha_aplicada),
            'proxima_dosis': str(v.proxima_dosis),
            'lote': v.lote,
            'animal': v.animal.nombre,
        })
    return JsonResponse(data, safe=False)

@login_required
def api_mis_mascotas(request):
    animales = Animal.objects.filter(dueno__email=request.user.email)
    data = []
    for animal in animales:
        citas = Cita.objects.filter(animal=animal)
        vacunas = Vacuna.objects.filter(animal=animal)
        data.append({
            'id': animal.id,
            'nombre': animal.nombre,
            'especie': animal.especie,
            'raza': animal.raza,
            'edad': animal.edad,
            'foto': request.build_absolute_uri(animal.foto.url) if animal.foto else None,
            'citas': [{'fecha': str(c.fecha), 'motivo': c.motivo, 'estado': c.estado} for c in citas],
            'vacunas': [{'nombre': v.nombre, 'proxima_dosis': str(v.proxima_dosis)} for v in vacunas],
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def api_solicitud_adopcion(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Debes iniciar sesion para adoptar'}, status=401)
        data = json.loads(request.body)
        animal = get_object_or_404(Animal, pk=data.get('animal_id'))

        solicitud = SolicitudAdopcion.objects.create(
            nombre=data.get('nombre'),
            dni=data.get('dni'),
            telefono=data.get('telefono'),
            email=data.get('email'),
            direccion=data.get('direccion'),
            tipo_vivienda=data.get('tipo_vivienda'),
            tiene_jardin=data.get('tiene_jardin'),
            otros_animales=data.get('otros_animales'),
            horas_en_casa=data.get('horas_en_casa'),
            experiencia=data.get('experiencia'),
            animal=animal,
        )

        animal.estado = 'adoptado'
        animal.save()

        return JsonResponse({
            'mensaje': f'Solicitud de adopcion para {animal.nombre} enviada correctamente',
            'solicitud_id': solicitud.id
        })
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

    # ==================== BIENVENIDA ====================

def bienvenida(request):
    return render(request, 'adopciones/bienvenida.html')