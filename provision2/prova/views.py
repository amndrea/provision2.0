from django.shortcuts import render
from .models import *

# Create your views here.

import openpyxl
from django.apps import apps
from django.db import transaction
import os


def importa_dati_da_file_excel(file_path, modello):

    # Controlla l'estensione del file
    _, file_extension = os.path.splitext(file_path)
    valid_extensions = ['.xlsx', '.xls', '.xlsm']
    
    if file_extension.lower() not in valid_extensions:
        print("Errore, il file deve essere in formato excel")
        return "Errore, il file deve essere in formato excel"

    Model = apps.get_model(modello)
    
    try:
        workbook = openpyxl.load_workbook(file_path)
    except openpyxl.utils.exceptions.InvalidFileException:
        print("il file non è un file excel valido o è corrotto")
        raise ValueError("Il file non è un file Excel valido o è corrotto.")
    
    sheet = workbook.active
    
    header = [cell.value for cell in sheet[1]]
    
    model_fields = [field.name for field in Model._meta.fields if field.name != 'id']
    
    if set(header) != set(model_fields):
        print("Errore, il file deve essere in formato excel")
        return "Errore, il file ed il modello non corrispondono"
        
    objects_to_create = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        data = dict(zip(header, row))
        objects_to_create.append(Model(**data))
    
    with transaction.atomic():
        Model.objects.bulk_create(objects_to_create)
    
    print("oggetti creati ", len(objects_to_create))
    return "OK"




def import_url(request):
    if request.method == "GET":
        return render(request, template_name="prova/import.html")
    
    if request.method == "POST":
        print("sono nella post") 
        