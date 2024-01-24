from django.shortcuts import render
from django.urls import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings 
import requests

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required
def profile(request):
    puuid = get_summoner('Bentinho','6038')
    return render(request, 'users-profile.html')

def get_summoner(summoner_name, summoner_tag):
    format_name = summoner_name.replace(" ", "%20")
    # Crie a URL da API para buscar as informações do invocador
    url = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{summoner_tag}?api_key={settings.RIOT_API_KEY}'

    # Faça a solicitação à API
    response = requests.get(url)

    # Verifique se a solicitação foi bem-sucedida
    if response.status_code == 200:
        summoner_info = response.json()
        summoner_puuid = summoner_info['puuid']

    return summoner_puuid