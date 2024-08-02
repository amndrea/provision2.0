# FILE ALL'INTERNO DEL QUALE SONO DEFINITE LE FUNZIONI UTILI AL FUNZIONAMENTO DELL'APPLICAZIONE

from .models import *


# Funzioni per controllare l'esistenza di un fornitore durante la modifica 
def check_esistenza_fornitore_nome(nome):
    return Fornitore.objects.filter(fornitore_nome=nome).exists()

def check_esistenza_fornitore_as(cod_as):
    return Fornitore.objects.filter(fornitore_cod_as=cod_as).exists()


def check_esistenza_societa(nome):
    return Societa.objects.filter(societa_nome=nome).exists()