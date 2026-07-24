from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from adopciones import views

urlpatterns = [
    path('', views.bienvenida, name='bienvenida'),
    path('admin/', admin.site.urls),
    path('adopciones/', include('adopciones.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)