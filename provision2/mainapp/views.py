from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse
from django.db.models import Q, ProtectedError
from django.core.paginator import Paginator
from .models import Fornitore, Magazzino, Mezzo, Tipologia, Zona, Listino, InserimentoFallito
from openpyxl import load_workbook
import pandas as pd
import json
import io
from django.shortcuts import render
from django.contrib import messages
from .models import Fornitore


def situazione_fornitori(request):
    # Ottieni tutti i fornitori ordinati per nome
    all_fornitori = Fornitore.objects.all().order_by('fornitore_nome')
    
    # Imposta la paginazione
    paginator = Paginator(all_fornitori, 10)  # 10 fornitori per pagina
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    if request.method == 'POST':
        # Gestione dell'aggiunta di un nuovo fornitore
        nome = request.POST.get('fornitore_nome')
        cod_as = request.POST.get('fornitore_cod_as')

        if not nome or not cod_as:
            messages.error(request, 'I campi non possono essere vuoti')
        elif Fornitore.objects.filter(fornitore_cod_as=cod_as).exists():
            messages.error(request, 'Il codice AS è già presente')
        else:
            new_fornitore = Fornitore(fornitore_nome=nome, fornitore_cod_as=cod_as)
            new_fornitore.save()
            messages.success(request, 'Fornitore aggiunto con successo')
            return redirect('mainapp:situazione_fornitori')

    return render(request, 'mainapp/situazione_fornitori.html', context)

# Funzione per eliminare un fornitore (opzionale)
def elimina_fornitore(request, pk):
    if request.method == 'POST':
        fornitore = get_object_or_404(Fornitore, pk=pk)
        try:
            fornitore.delete()
            messages.success(request, 'Fornitore eliminato con successo')
        except ProtectedError:
            listini_associati = Listino.objects.filter(fornitore=fornitore).count()
            messages.error(request, f'Impossibile eliminare il fornitore. Ci sono {listini_associati} listini associati.')
    
    return redirect('mainapp:situazione_fornitori')




















# -------------------------------------------------------------------------------------------------------------- #
# ---------------------------- GESTIONE CARICAMENTO DEL LISTINO ATTRAVERSO FILE EXCEL -------------------------- #
# -------------------------------------------------------------------------------------------------------------- #
class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)
    

class ImportListinoView(View):
    template_name = 'mainapp/import_listino.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        if 'file' not in request.FILES:
            messages.error(request, 'Nessun file caricato')
            return redirect('mainapp:import_listino')
        
        excel_file = request.FILES['file']
        print(excel_file)

        try:
            # Leggo il file in memoria
            file_in_memory = io.BytesIO(excel_file.read())
            
            # carico il workbook
            wb = load_workbook(filename=file_in_memory, read_only=True, data_only=True)
            
            # primo foglio
            sheet = wb.active
            
            # converto il foglio in un DataFrame pandas
            data = sheet.values
            columns = next(data)
            df = pd.DataFrame(data, columns=columns)

        except Exception as e:
            print("Errore nel leggere il file")
            print(f"Errore specifico: {type(e).__name__}, {str(e)}")
            messages.error(request, f'Errore nel leggere il file Excel: {str(e)}')
            return redirect('mainapp:import_listino')
        
        # Verifica che il file abbia tutte le colonne
        required_columns = ['FORNITORE', 'MAGAZZINO', 'MEZZO', 'TIPOLOGIA', 'PARTENZA', 'ARRIVO', 'COSTO', 'DATA', 'CONTOCONTABILE', 'VOCESPESA', 'CENTROCOSTO']
        if not all(col in df.columns for col in required_columns):
            print("mancano delle colonne nel file")
            messages.error(request, 'Il file non contiene tutte le colonne richieste')
            return redirect('mainapp:import_listino')
        
        righe_inserite = 0
        righe_aggiornate = 0
        righe_fallite = 0
    
        for _, row in df.iterrows():
            try:
                with transaction.atomic():
                    # Cerco di ottenere le entità esistenti
                    try:
                        fornitore = Fornitore.objects.get(fornitore_nome=row['FORNITORE'])
                        magazzino = Magazzino.objects.get(magazzino_nome=row['MAGAZZINO'])
                        mezzo = Mezzo.objects.get(mezzo_nome=row['MEZZO'])
                        tipologia = Tipologia.objects.get(tipologia_nome=row['TIPOLOGIA'])
                        partenza = Zona.objects.get(zona_nome=row['PARTENZA'])
                        arrivo = Zona.objects.get(zona_nome=row['ARRIVO'])
                    except ObjectDoesNotExist as e:
                        # Se una qualsiasi entità non esiste, sollevo un'eccezione
                        raise ValueError(f"Entità non trovata: {str(e)}")

                    listino, created = Listino.objects.update_or_create(
                        fornitore=fornitore,
                        magazzino=magazzino,
                        mezzo=mezzo,
                        tipologia=tipologia,
                        partenza=partenza,
                        arrivo=arrivo,
                        defaults={
                            'costo': row['COSTO'],
                            'data_ultimo_aggiornamento': row['DATA'],
                            'conto_contabile': row['CONTOCONTABILE'],
                            'voce_spesa': row['VOCESPESA'],
                            'centro_costo': row['CENTROCOSTO']
                        }
                    )
                    
                    if created:
                        righe_inserite += 1
                    else:
                        righe_aggiornate += 1

            except Exception as e:
                righe_fallite += 1
                dati_riga = row.to_dict()

                # Converto esplicitamente la colonna 'DATA' in stringa
                if 'DATA' in dati_riga and isinstance(dati_riga['DATA'], pd.Timestamp):
                    dati_riga['DATA'] = dati_riga['DATA'].strftime('%Y-%m-%d %H:%M:%S')
                
                try:
                    with transaction.atomic():
                        InserimentoFallito.objects.create(
                            dati_riga=json.dumps(dati_riga, cls=CustomJSONEncoder),
                            errore=str(e)
                        )
                    print(f"Inserimento fallito creato: {dati_riga}")
                except Exception as inner_e:
                    print(f"Errore durante la creazione di InserimentoFallito: {str(inner_e)}")

        if righe_fallite > 0:
             messages.warning(request, f'Importazione completata. Inserite: {righe_inserite}, '
                                  f'Aggiornate: {righe_aggiornate}, Fallite: {righe_fallite}')
        else:    
            messages.success(request, f'Importazione completata. Inserite: {righe_inserite}, '
                                  f'Aggiornate: {righe_aggiornate}, Fallite: {righe_fallite}')
        return redirect('mainapp:import_listino')



# -------------------------------------------------------------------------------------------------------------- #
# ---------------------------- Gestione righe fallite  -------------------------- #
# -------------------------------------------------------------------------------------------------------------- #
class InserimentoFallitoListView(ListView):
    model = InserimentoFallito
    paginate_by = 20
    template_name = "mainapp/listino_falliti.html"
    context_object_name = "lista_falliti"

    def get_queryset(self):
        queryset = super().get_queryset()
        
        data_tentativo = self.request.GET.get('data_tentativo')
        tipo_errore = self.request.GET.get('tipo_errore')

        if data_tentativo:
            queryset = queryset.filter(data_tentativo__gte=data_tentativo)
        if tipo_errore:
            queryset = queryset.filter(errore__icontains=tipo_errore)

        return queryset.order_by('-data_tentativo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_tentativo'] = self.request.GET.get('data_tentativo', '')
        context['tipo_errore'] = self.request.GET.get('tipo_errore', '')
        return context

class EliminaInserimentoFallitoView(View):
    def post(self, request, pk):
        print("sono in questa post")
        print("PK = ", pk)
        oggetto = get_object_or_404(InserimentoFallito, pk=pk)
        oggetto.delete()
        messages.success(request, "L'inserimento fallito è stato eliminato con successo.")
        return redirect(reverse('mainapp:listino_falliti'))

class DeleteAllInserimentiFallitiView(View):
    def get(self, request):
        InserimentoFallito.objects.all().delete()
        messages.success(request, "Tutti gli inserimenti falliti sono stati cancellati con successo.")
        return redirect(reverse('mainapp:listino_falliti'))