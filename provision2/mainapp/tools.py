# FILE ALL'INTERNO DEL QUALE SONO DEFINITE LE FUNZIONI 
# UTILI AL FUNZIONAMENTO DELL'APPLICAZIONE

from .models import *
import os
from django.conf import settings
from datetime import date


# Funzioni per controllare l'esistenza di un fornitore durante la modifica 
def check_esistenza_fornitore_nome(nome):
    return Fornitore.objects.filter(fornitore_nome=nome).exists()

def check_esistenza_fornitore_as(cod_as):
    return Fornitore.objects.filter(fornitore_cod_as=cod_as).exists()


def check_esistenza_societa(nome):
    return Societa.objects.filter(societa_nome=nome).exists()

def check_esistenza_zona(nome):
    return Zona.objects.filter(zona_nome=nome).exists()

def check_esistenza_riga_listino(fornitore, magazzino, mezzo, tipologia, partenza, arrivo):
    return Listino.objects.filter(
        fornitore=fornitore,
        magazzino=magazzino,
        mezzo=mezzo,
        tipologia=tipologia,
        partenza=partenza,
        arrivo=arrivo
    )



def log_to_file(message):
    log_dir = os.path.join(settings.MEDIA_ROOT, 'log')
    os.makedirs(log_dir, exist_ok=True)
    log_file_name = f"{date.today().isoformat()}_import.txt"
    log_file_path = os.path.join(log_dir, log_file_name)
    
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{message}\n")
    