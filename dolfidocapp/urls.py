from django.contrib import admin
from django.urls import path
from . import views  # Importa as views da sua aplicação


urlpatterns = [
    path('admin/', admin.site.urls),  # URL para acessar a área administrativa do Django
    path('', views.index, name='home'),  # URL raiz que será aberta ao acessar o site
    path('medinfo', views.medInfo, name='medinfo'),
]
