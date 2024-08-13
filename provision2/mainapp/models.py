from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.

# -------------------------------------------------------------------------------------------- #
# prima colonna del listino, il fornitore che effettua il trasporto
class Fornitore(models.Model):
    fornitore_nome = models.CharField(max_length=128, blank=False, null=False, unique=False)
    fornitore_cod_as = models.CharField(max_length=8, blank=False, null=False, unique=True)

# -------------------------------------------------------------------------------------------- #

class Societa(models.Model):
    societa_nome = models.CharField(max_length=128, blank=False, null=False, unique=True)


# -------------------------------------------------------------------------------------------- #
# seconda colonna del listino, magazzino 
class Magazzino(models.Model):
    magazzino_nome = models.CharField(max_length=128, blank=False, null=False)
    magazzino_lettera = models.CharField(max_length=1, blank=False, null=False, unique=True)
    # per separare i magazzini sui quali gli utenti sono abilitati 
    societa = models.ManyToManyField(Societa)
# -------------------------------------------------------------------------------------------- #



# -------------------------------------------------------------------------------------------- #
# terza colonna del listino, mezzo con il quale vinene effettuato il trasporto
class Mezzo(models.Model):
    mezzo_nome = models.CharField(max_length=128, blank=False, null=False, unique=True)
# -------------------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------------------- #
# tipologia di trasporto 
class Tipologia(models.Model):
    tipologia_nome = models.CharField(max_length=128, blank=False, null=False, unique=True)
# -------------------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------------------- #
# Classe che implementa le zone, utilizzate per definire zone di partenza e di arrivo
class Zona(models.Model):
    zona_nome = models.CharField(max_length=128, blank=False, null=False, unique=True)
# -------------------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------------------- #
# Classe che definisce il listino. 
# Le istanze di questa classe possono essere definite in maniera massiva tramite import o 
# singolarmente tramite maschera 
class Listino(models.Model):
    # impedisce l'eliminazione di un Fornitore se ci sono istanze di Listino che lo referenziano.
    fornitore = models.ForeignKey(Fornitore, on_delete=models.PROTECT)
    magazzino = models.ForeignKey(Magazzino, on_delete=models.PROTECT) # mag = chi ti sta addebitando il viaggio
    mezzo = models.ForeignKey(Mezzo, on_delete=models.PROTECT)
    tipologia = models.ForeignKey(Tipologia, on_delete=models.PROTECT)
    partenza = models.ForeignKey(Zona, related_name="partenza", on_delete=models.PROTECT)
    arrivo = models.ForeignKey(Zona, related_name="arrivo", on_delete=models.PROTECT)

    # data utilizzata per la validità 
    data_ultimo_aggiornamento = models.DateField(default=datetime.date(1997, 12, 23))
    costo = models.FloatField(default=0.0)

    # Anche questi vanno tabellati
    conto_contabile = models.CharField(max_length=25, default = '-')
    voce_spesa = models.CharField(max_length=10, blank=False, null=False)
    centro_costo = models.CharField(max_length=10, blank=False, null=False)
    data_upload = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('fornitore', 'magazzino', 'mezzo', 'tipologia', 'partenza', 'arrivo')


# -------------------------------------------------------------------------------------------- #

class InserimentoFallito(models.Model):
    dati_riga = models.JSONField()  
    errore = models.TextField()  
    data_tentativo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Errore: {self.errore[:50]}... - Data: {self.data_tentativo}"

# -------------------------------------------------------------------------------------------- #
#class Fattura(models.Model):
# -------------------------------------------------------------------------------------------- #
# FORNITORE lo potrei ricavare dalle righe del listino, ma per questione di ottimizzazione lo metto qua
class Prefattura(models.Model):
    fattura_numero = models.IntegerField()
    fattura_data = models.DateField()
    fattura_documento = models.FileField(upload_to='documenti/')

    fattura_fornitore = models.ForeignKey(Fornitore, on_delete=models.PROTECT)
    fattura_utente = models.ForeignKey(User, on_delete=models.PROTECT)

    data_modifica = models.DateField(auto_now=True)
    # Nella fattura sono group_by (Centro Costo, Voce Spesa, Conto Contabile iniseme, queste fanno un unica riga della fattura)
    # magazzino
    # importo => somma di tutti gli importi del documento



class PrefatturaRighe(models.Model):
    prefattura = models.ForeignKey(Prefattura, on_delete=models.PROTECT)
    riga_listino = models.ForeignKey(Listino, on_delete=models.PROTECT)
    quantita = models.IntegerField()
