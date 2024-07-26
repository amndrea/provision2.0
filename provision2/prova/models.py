from django.db import models

# Create your models here.
class ClasseDiTest(models.Model):
    nome = models.CharField(max_length=128, blank=True, null=True)
    eta = models.IntegerField(default=0)
    stato = models.CharField(max_length=128)
