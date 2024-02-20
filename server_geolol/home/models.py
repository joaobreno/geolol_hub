from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Invocador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_invocador = models.CharField(max_length=50, blank=True)
    tag = models.CharField(max_length=10, blank=True)
    profile_icon = models.CharField(max_length=10, blank=True)
    puuid = models.CharField(max_length=100, blank=True)

    # Adicione outros atributos conforme necessário

    def __str__(self):
        return self.user.username