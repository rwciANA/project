from django import forms
from .models import Animal, Dueno, SolicitudAdopcion, Cita, Vacuna


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nombre', 'especie', 'raza', 'edad', 'foto', 'descripcion', 'estado', 'dueno']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del animal'}),
            'especie': forms.Select(
                choices=[('', 'Selecciona una especie'), ('Perro', 'Perro'), ('Gato', 'Gato')],
                attrs={'class': 'form-select'}
            ),
            'raza': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Labrador, Siamés'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 30}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe al animal...'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'dueno': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {'dueno': 'Dueño', 'descripcion': 'Descripción'}

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad is None or edad < 0 or edad > 30:
            raise forms.ValidationError("La edad debe estar entre 0 y 30 años")
        return edad

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if any(char.isdigit() for char in nombre):
            raise forms.ValidationError("El nombre no puede contener números")
        return nombre


class DuenoForm(forms.ModelForm):
    class Meta:
        model = Dueno
        fields = ['nombre', 'apellido', 'dni', 'telefono', 'email', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '987654321'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@email.com'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Direccion completa'}),
        }

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni.isdigit() or len(dni) != 8:
            raise forms.ValidationError("El DNI debe tener exactamente 8 numeros")
        return dni

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit() or len(telefono) != 9:
            raise forms.ValidationError("El telefono debe tener exactamente 9 numeros")
        return telefono


class SolicitudAdopcionForm(forms.ModelForm):
    class Meta:
        model = SolicitudAdopcion
        fields = ['nombre', 'dni', 'telefono', 'email', 'direccion',
                  'tipo_vivienda', 'tiene_jardin', 'otros_animales',
                  'horas_en_casa', 'experiencia', 'animal']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '987654321'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@email.com'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'tipo_vivienda': forms.Select(attrs={'class': 'form-select'}),
            'tiene_jardin': forms.Select(attrs={'class': 'form-select'}),
            'otros_animales': forms.Select(attrs={'class': 'form-select'}),
            'horas_en_casa': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 24}),
            'experiencia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe tu experiencia con animales...'
            }),
            'animal': forms.Select(attrs={'class': 'form-select'}),
        }


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha', 'hora', 'motivo', 'observaciones', 'estado', 'animal', 'veterinario']
        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'min': '2020-01-01',
                    'max': '2100-12-31',
                }
            ),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'motivo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Motivo de la cita...'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales...'
            }),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'animal': forms.Select(attrs={'class': 'form-select'}),
            'veterinario': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')

        if fecha.year < 2020 or fecha.year > 2100:
            raise forms.ValidationError(
                "El año debe estar entre 2020 y 2100."
            )

        return fecha


class VacunaForm(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = ['nombre', 'fecha_aplicada', 'proxima_dosis', 'lote', 'animal']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la vacuna'
            }),
            'fecha_aplicada': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'min': '2020-01-01',
                    'max': '2100-12-31',
                }
            ),
            'proxima_dosis': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'min': '2020-01-01',
                    'max': '2100-12-31',
                }
            ),
            'lote': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numero de lote'
            }),
            'animal': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_fecha_aplicada(self):
        fecha = self.cleaned_data.get('fecha_aplicada')

        if fecha.year < 2020 or fecha.year > 2100:
            raise forms.ValidationError(
                "El año debe estar entre 2020 y 2100."
            )

        return fecha

    def clean_proxima_dosis(self):
        fecha = self.cleaned_data.get('proxima_dosis')

        if fecha.year < 2020 or fecha.year > 2100:
            raise forms.ValidationError(
                "El año debe estar entre 2020 y 2100."
            )

        return fecha