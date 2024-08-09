from django.contrib.auth.models import Group

from email.mime.text import MIMEText
from smtplib import SMTPRecipientsRefused
import smtplib
import hashlib
import re
import time

INDIRIZZO_FROM = 'a.bonfatti@gruppoconcorde.it'


# Funzione che utilizzo nella validazione della password per vedere se una stringa contiene un carattere speciale
def contiene_carattere_speciale(stringa):
    regex = re.compile(r'[^a-zA-Z0-9]')  # qualsiasi carattere non alfanumerico
    return bool(regex.search(stringa))


# Funzione che utilizzo nella validazione della password per vedere se una stringa contiene una lettera maiuscola
def contiene_maiuscola(stringa):
    regex = re.compile(r'[A-Z]')   # lettera maiuscola
    return bool(regex.search(stringa))


def send_mail(indirizzo_to, oggetto, testo):

    testo = testo + "\nEmail generata in maniera automatica, non rispondere a questa email \n\n"
    messaggio = f"Subject: {oggetto}\n\n{testo}"

    email =smtplib.SMTP('smtp.gruppoconcorde.it', 25)
    email.sendmail(INDIRIZZO_FROM, indirizzo_to, messaggio)
    email.quit()


def generate_reset_token(user_id):
    # Chiave segreta per la generazione del token
    secret_key = 'il_tuo_segreto'

    # Creazione del token basato sull'ID dell'utente e un timestamp
    token_data = f'{user_id}_{time.time()}_{secret_key}'

    # Generazione hash del token
    token_hash = hashlib.sha256(token_data.encode()).hexdigest()
    return token_hash