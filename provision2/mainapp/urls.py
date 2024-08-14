from django.urls import path
from .views import *

app_name = 'mainapp'
urlpatterns = [

    # URL PER LE ANAGRAFICHE FORNITORI
    path("situazione_fornitori/",situazione_fornitori,name="situazione_fornitori"),
    path("elimina_fornitore/<int:pk>/",elimina_fornitore,name="elimina_fornitore"),
    path('modifica-fornitore/<int:pk>/', modifica_fornitore, name='modifica_fornitore'),

    # URL PER LE ANAGRAFICHE DELLE SOCIETA'
    path("situazione_societa/",situazione_societa,name="situazione_societa"),
    path("elimina_societa/<int:pk>/",elimina_societa,name="elimina_societa"),
    path('modifica-societa/<int:pk>/', modifica_societa, name='modifica_societa'),

    path('magazzini/',situazione_magazzini, name='situazione_magazzini'),
    path('magazzini/modifica/<int:pk>/', modifica_magazzino, name='modifica_magazzino'),
    path('magazzini/elimina/<int:pk>/', elimina_magazzino, name='elimina_magazzino'),

    path('mezzi/',situazione_mezzi, name='situazione_mezzi'),
    path('mezzi/modifica/<int:pk>/', modifica_mezzo, name='modifica_mezzo'),
    path('mezzi/elimina/<int:pk>/', elimina_mezzo, name='elimina_mezzo'),

    path('tipologie/', situazione_tipologie, name='situazione_tipologie'),
    path('tipologie/modifica/<int:pk>/', modifica_tipologia, name='modifica_tipologia'),
    path('tipologie/elimina/<int:pk>/', elimina_tipologia, name='elimina_tipologia'),

    path('zone/', situazione_zone, name='situazione_zone'),
    path('zone/modifica/<int:pk>/', modifica_zona, name='modifica_zona'),
    path('zone/elimina/<int:pk>/', elimina_zona, name='elimina_zona'),
    path('import_zone/', ImportZone.as_view(), name="import_zone"),




    # URL al quale importo un listino da un file excel 
    path('import-listino/', ImportListinoView.as_view(), name='import_listino'),
    path('listino/',ListinoListView.as_view(), name='listino'),
    # URL al quale visualizzo gli import falliti da listino
    path('listino_falliti/', InserimentoFallitoListView.as_view(), name='listino_falliti'),
    # URL al quale elimino un inserimento fallito 
    path('elimina_fallito/<int:pk>/', EliminaInserimentoFallitoView.as_view(), name='elimina_inserimento_fallito'),
    # URL con il quale eliminare tutte le righe fallite dal caricamento massivo di un listino falliti
    path('delete-all-inserimenti-falliti/', DeleteAllInserimentiFallitiView.as_view(), name='delete_all_inserimenti_falliti'),



    path('situazione_prefatture/',situazione_prefatture, name="situazione_prefatture"),
    path('aggiungi_prefattura/', aggiungi_prefattura, name='aggiungi_prefattura'),
    path('elimina_prefattura/<int:pk>/',elimina_prefattura, name="elimina_prefattura"),
    #path('edit_prefattura/<int:pk>/', edit_prefattura, name='edit_prefattura'),
    #path('filter_righe_listino/<int:pk>/', filter_righe_listino, name='filter_righe_listino'),
    path('elimina_riga_prefattura/<int:pk>/',elimina_riga_prefattura, name="elimina_riga_prefattura"),

    path('new_edit_prefattura/<int:pk>/', new_edit_prefattura, name='new_edit_prefattura'),
    path('new_filter_righe_listino/', rew_filter_righe_listino, name='new_filter_righe_listino'),


]

