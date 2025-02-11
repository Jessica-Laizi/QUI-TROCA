"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inventario.views import index, add, save, show, delete, perfil, listagem, details, save_item, pag_troca, categorias, logout_user, cadastro_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name = "login"), 
    path('form/', add, name="add"),
    path('form/save', save, name="save"),
    path('show/<int:id>', show, name="show"),
    path('delete/<int:id>', delete, name="delete"),
    path('perfil/', perfil, name="perfil"),
    path('inicial/', listagem, name="inicial"),
    path('details/<int:id>', details, name="details"),
    path('save_item/', save_item, name="save_item"),
    path('pag_troca/<str:info>', pag_troca, name="pag_troca"),
    path('categorias/<str:categoria>', categorias, name="categorias"),
    path('logout/', logout_user, name="logout"),
    path('cadastro_usuario/', cadastro_usuario, name="cadastro_usuario"),
     
    
      
]
