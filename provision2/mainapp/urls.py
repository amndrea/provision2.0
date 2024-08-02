from django.urls import path
from .views import *

app_name = 'mainapp'
urlpatterns = [

    # View per visualizzare la lista di fornitori ed inserire un nuovo fornitore
    path("situazione_fornitori/",situazione_fornitori,name="situazione_fornitori"),
    
    # View per eliminare un fornitore 
    path("elimina_fornitore/<int:pk>/",elimina_fornitore,name="elimina_fornitore"),
    
    # URL al quale importo un listino da un file excel 
    path('import-listino/', ImportListinoView.as_view(), name='import_listino'),

    # URL al quale visualizzo gli import falliti da listino
    path('listino_falliti/', InserimentoFallitoListView.as_view(), name='listino_falliti'),

    # URL al quale elimino un inserimento fallito 
    path('elimina_fallito/<int:pk>/', EliminaInserimentoFallitoView.as_view(), name='elimina_inserimento_fallito'),

    # URL con il quale eliminare tutte le righe fallite dal caricamento massivo di un listino falliti
    path('delete-all-inserimenti-falliti/', DeleteAllInserimentiFallitiView.as_view(), name='delete_all_inserimenti_falliti'),

]

