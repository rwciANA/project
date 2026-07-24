from django.db import models

class Dueno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=8)
    telefono = models.CharField(max_length=9)
    email = models.EmailField()
    direccion = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Dueño"
        verbose_name_plural = "Dueños"


class Veterinario(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)
    horario = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Veterinario"
        verbose_name_plural = "Veterinarios"


class Animal(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('adoptado', 'Adoptado'),
        ('en_tratamiento', 'En tratamiento'),
    ]
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=50)
    edad = models.IntegerField()
    foto = models.ImageField(upload_to='animales/', blank=True, null=True)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    dueno = models.ForeignKey(Dueno, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Vacuna(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_aplicada = models.DateField()
    proxima_dosis = models.DateField()
    lote = models.CharField(max_length=50)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.animal.nombre}"


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('atendida', 'Atendida'),
        ('cancelada', 'Cancelada'),
    ]
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()
    observaciones = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    veterinario = models.ForeignKey(Veterinario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cita {self.fecha} - {self.animal.nombre}"

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"

class SolicitudAdopcion(models.Model):
    TIPO_VIVIENDA_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('otro', 'Otro'),
    ]
    SI_NO_CHOICES = [
        ('si', 'Si'),
        ('no', 'No'),
    ]
    nombre = models.CharField(max_length=200)
    dni = models.CharField(max_length=8)
    telefono = models.CharField(max_length=9)
    email = models.EmailField()
    direccion = models.TextField()
    tipo_vivienda = models.CharField(max_length=20, choices=TIPO_VIVIENDA_CHOICES)
    tiene_jardin = models.CharField(max_length=3, choices=SI_NO_CHOICES)
    otros_animales = models.CharField(max_length=3, choices=SI_NO_CHOICES)
    horas_en_casa = models.IntegerField()
    experiencia = models.TextField()
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.animal.nombre}"

    class Meta:
        verbose_name = "Solicitud de Adopcion"
        verbose_name_plural = "Solicitudes de Adopcion"