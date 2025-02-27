from django.contrib import admin
from .models import *

# Register your models here.
class PhantomRanksAdmin(admin.ModelAdmin):
    list_display = ['summonerName', 'puuid', 'summonerId']

admin.site.register(PhantomRanks, PhantomRanksAdmin)