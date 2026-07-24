from django.contrib import admin

from .models import Animal, SolicitudAdopcion, Vacuna, Cita, Dueno, Veterinario

admin.site.register(Animal)
admin.site.register(Vacuna)
admin.site.register(Cita)
admin.site.register(Dueno)
admin.site.register(Veterinario)
admin.site.register(SolicitudAdopcion)