from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from mainapp.models import Societa


class UserHashPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hash_password = models.CharField(max_length=127, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Verifica se il token è scaduto, scade dopo 24 ore
        expiration_date = self.creation_date + timezone.timedelta(hours=24)
        return timezone.now() <= expiration_date
    

# Tabella di relazione tra un utente e le societa. Un utente può appartenere a diverse societa
class UserSocieta(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    societa = models.ForeignKey(Societa, on_delete=models.CASCADE)