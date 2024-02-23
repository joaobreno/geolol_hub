from django.shortcuts import render, redirect, get_object_or_404
from django.urls import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings 
import requests
from .decorator import *
from .models import *
import cassiopeia as cass
import arrow
import datetime
import json

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required
@profile_user_data
def profile(request, context_dict):
    # puuid = get_summoner('Bentinho','6038')
    # data_match = get_data_match('BR1_2891213898')
    tier_data = get_object_or_404(Ranks, summoner=context_dict['user'].invocador.id)
    context_dict['tiers'] = tier_data


    match = Matches.objects.all().first()
    context_dict['match'] = json.loads(match.data_json)


    return render(request, 'users-profile.html', context_dict)



def get_data_match(match):
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match}?api_key={settings.RIOT_API_KEY}'
    agora = datetime.datetime.now()
    # Faça a solicitação à API
    response = requests.get(url)

    # Verifique se a solicitação foi bem-sucedida
    if response.status_code == 200:
        match_info = response.json()

    return match_info


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