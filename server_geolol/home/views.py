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
from riot_admin import models

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


    matches = Matches.objects.all()
    matches_data = []
    for match in matches:
        matches_data.append(SummonerMatch(match.matchID, context_dict['user'].invocador.puuid))


    context_dict['matches'] = matches_data

    # cass.set_riot_api_key("")
    # summoner = cass.get_summoner(name="The Bentin", region="BR")


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



class SummonerMatch:
    def __init__(self, match_id, puuid):
        match = get_object_or_404(Matches, matchID=match_id)
        data = json.loads(match.data_json)
        blue_side_participants = []
        red_side_participants = []
        for index, participant in enumerate(data['info']['participants']):
            if participant['teamId'] == 100:
                blue_side_participants.append(participant)
            if participant['teamId'] == 200:
                red_side_participants.append(participant)
            if participant['puuid'] == puuid:
                self.mainSummoner = participant
                self.mainSpells = {'spellD': participant['summoner1Id'], 'spellF': participant['summoner2Id']}
                self.mainRuneKeystone = participant['perks']['styles'][0]['selections'][0]['perk']
                self.mainRuneSubStyle = participant['perks']['styles'][1]['style']
                self.mainKDA = {'kills': participant['kills'], 'deaths': participant['deaths'], 'assists': participant['assists']}
                self.teamID = participant['teamId']
                self.visionScore = participant['visionScore']
                self.mainSummonerItems = [participant['item0'], participant['item1'], participant['item2'], participant['item3'], participant['item4'], participant['item5']]
                self.mainSummonerTrinket = participant['item6']
                if participant['teamId'] == 100 and data['info']['teams'][0]['win']:
                    self.mainResult = True
                else:
                    self.mainResult = False

        self.blue_side = {'participants': blue_side_participants, 'data': data['info']['teams'][0]}
        self.red_side = {'participants': red_side_participants, 'data': data['info']['teams'][1]}
        self.gameStartTime = datetime.datetime.fromtimestamp(data['info']['gameStartTimestamp'] / 1000.0)
        self.gameEndTime = datetime.datetime.fromtimestamp(data['info']['gameEndTimestamp'] / 1000.0)
        self.gameDuration = data['info']['gameDuration']
        self.queueId = data['info']['queueId']
        self.id = match.id



    def str_gameDuration(self):
        minutes = self.gameDuration // 60
        seconds = self.gameDuration % 60
        return f"{minutes}:{seconds:02d}"
    
    def str_match_timeago(self):
        time = datetime.datetime.now() - self.gameEndTime
        return time.days
    
    def str_gameResult(self):
        return 'Vitória' if self.mainResult else 'Derrota'
    
    def type_queue(self):
        type_dict = {
            420: 'Ranqueada Solo',
            440: 'Ranqueada Flexível'
        }
        if self.queueId in type_dict:
            return type_dict[self.queueId]
        else:
            return 'Indeterminado'
        
    def spellD_icon(self):
        if self.mainSpells['spellD'] in settings.ICON_SPELL_DICT:
            return settings.ICON_SPELL_DICT[self.mainSpells['spellD']]
        
    def spellF_icon(self):
        if self.mainSpells['spellF'] in settings.ICON_SPELL_DICT:
            return settings.ICON_SPELL_DICT[self.mainSpells['spellF']]
        
    def kda_ratio(self):
        kda_ratio = (self.mainKDA['kills'] + self.mainKDA['assists']) / self.mainKDA['deaths']
        return '{:.2f}'.format(kda_ratio)

    def kill_presence(self):
        team = self.blue_side if self.teamID == 100 else self.red_side
        kp = ((self.mainKDA['kills'] + self.mainKDA['assists']) / (team['data']['objectives']['champion']['kills'])) * 100
        return '{:.0f}%'.format(kp)
    
    def cs_per_minute(self):
        time = self.gameEndTime - self.gameStartTime
        cs = self.mainSummoner['totalMinionsKilled'] / (time.seconds / 60)
        return '{:.1f}'.format(cs) 