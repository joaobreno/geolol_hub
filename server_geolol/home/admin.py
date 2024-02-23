from django.contrib import admin
from .models import *
# Register your models here.

class InvocadorAdmin(admin.ModelAdmin):
    list_display = ['user', 'nome_invocador', 'tag']

admin.site.register(Invocador, InvocadorAdmin)

class RanksAdmin(admin.ModelAdmin):
    list_display = ['summoner', 'soloqueue_tier', 'soloqueue_rank', 'flexqueue_tier', 'flexqueue_rank']

admin.site.register(Ranks, RanksAdmin)

class MatchesAdmin(admin.ModelAdmin):
    list_display = ['matchID', 'gameMode', 'gameVersion']

admin.site.register(Matches, MatchesAdmin)