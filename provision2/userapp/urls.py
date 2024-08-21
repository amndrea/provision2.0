from django.urls import path
from .views import *
app_name = "userapp"

urlpatterns = [
    # URL al quale creo un nuovo utente
    path('crea_utente', crea_utente, name="crea_utente"),

    # URL inviato per mail alla quale un utente resetta la propria password
    path('reset_password/<str:reset_token>/', reset_password, name="reset_password"),

    path('users/', UserListView.as_view(), name='user_list'),
    path('elimina_utente/<int:utente_pk>/',elimina_utente,name="elimina_utente"),

    path('send_reset_password/<int:user_pk>/', send_reset_password, name="send_reset_password"),

    path('situazione_utente_societa/<int:utente_pk>/', situazione_utente_societa, name='situazione_utente_societa'),
    path('delete-societa-utente/<int:societa_pk>/<int:utente_pk>/', delete_societa_utente, name='delete_societa_utente'),
]