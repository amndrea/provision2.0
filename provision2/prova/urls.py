from django.urls import path
from .views import *

app_name = 'prova'
urlpatterns = [

    path('import_url', import_url, name="import_url")

]