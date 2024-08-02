from django.urls import path
from .views import *
app_name = "UserApp"

urlpatterns = [

]
"""
    # ---------------------------------------------------------------------------------------------------------------------- #
    # URL al quale creo un nuovo utente
    path('crea_utente', crea_utente, name="crea_utente"),
    # URL al quale arrivo per resettare la password
    path('reset_password/<str:reset_token>/', reset_password, name="reset_password"),
    path('send_reset_password/<int:user_pk>/', send_reset_password, name="send_reset_password"),
    # URL AL QUALE VISUALIZZO GLI UTENTI
    path('lista_utenti/<str:messaggio>/', lista_utenti, name='lista_utenti'),
    # URL al qualre promuovo un utente da utente base ad expert
    path('promuovi_utente/<int:user_pk>/',promuovi_utente, name='promuovi_utente'),
    # URl for delete a user given the user pk
    path('delete_user/<int:user_pk>/', delete_user, name="delete_user"),
    #  
"""