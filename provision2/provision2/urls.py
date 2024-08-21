"""
URL configuration for provision2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),

    # URL al quale si visualizza il form di login
    path("", login_view, name="login"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # URL per la home dell'utente loggato 
    path("home", home, name="home"),
    
    # URL al quale scarico il tempalte per i nuovi inserimenti
    path('download-template/', download_template, name='download_template'),


    path("main/",include("mainapp.urls")),
    path("user/", include("userapp.urls"))


    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# DA includere in fase di testing con il server locale per servire immagii 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
