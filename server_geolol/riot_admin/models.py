from django.db import models


class AdminSet(models.Model):
    riot_api_key = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.pk and AdminSet.objects.exists():
            return
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