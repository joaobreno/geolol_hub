from django.db import models
import requests


class AdminSet(models.Model):
    riot_api_key = models.CharField(max_length=100)
    status_key = models.BooleanField(default=False)
    current_patch = models.CharField(max_length=20, default='')

    def save(self, *args, **kwargs):
        if not self.pk and AdminSet.objects.exists():
            return
        
        url = "https://ddragon.leagueoflegends.com/api/versions.json"
        response = requests.get(url)

        if response.status_code == 200:
            versions = response.json()
            self.current_patch = versions[0]
            
        super().save(*args, **kwargs)

    def __str__(self):
        return "Admin"


class AdminSetInstance(models.Model):
    singleton_model = models.OneToOneField(AdminSet, on_delete=models.CASCADE, primary_key=True)

    def save(self, *args, **kwargs):
        if AdminSetInstance.objects.exists():
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return "Instância do Admin"