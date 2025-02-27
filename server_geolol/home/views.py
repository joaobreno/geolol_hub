from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings 
from datetime import timedelta
from django.utils import timezone
from home.riot_api import *
from home.utils import _log_console_title_section, _log_console_item_section
from .forms import *
import requests
from .decorator import *
from .models import *
from .enums import *
import cassiopeia as cass
import arrow
import datetime
import json
from riot_admin import models
from .task import *
from celery import shared_task
from charts.models import PhantomRanks, DiaryRank
import hashlib

# Create your views here.

def index(request):
    return render(request, 'index.html')


@login_required
def register_summoner(request):
    if request.method == 'POST':
        form = RegisterSummonerForm(request.POST)
        if form.is_valid():
            ## Criando Invocador para o Usuário
            invocador, createdSummoner = Invocador.objects.update_or_create(
                user=request.user,
                defaults={
                    "nome_invocador": form.cleaned_data['summoner_name'],
                    "tag": form.cleaned_data['tagline'],
                    "puuid": form.cleaned_data['puuid'],
                    "summonerId": form.cleaned_data['summonerID'],
                    "profile_icon": form.cleaned_data['profileIcon'],
                    "level": form.cleaned_data['level'],
                    "summonerName": form.cleaned_data['summoner_name'],
                }
            )
            # Deletando PhantomRank
            if invocador and createdSummoner:
                try:
                    phantom = PhantomRanks.objects.get(puuid=invocador.puuid)
                    phantom.delete()
                except Invocador.DoesNotExist:
                    phantom = None

            # Criando Rank para o Invocador
            rank, createdRank = Ranks.objects.update_or_create(
                summoner=invocador,
                defaults={
                    "soloqueue_tier": 'UNRANKED',
                    "soloqueue_rank": '',
                    "soloqueue_leaguePoints": 0,
                    "soloqueue_wins": 0,
                    "soloqueue_losses": 0,

                    "flexqueue_tier": 'UNRANKED',
                    "flexqueue_rank": '',
                    "flexqueue_leaguePoints": 0,
                    "flexqueue_wins": 0,
                    "flexqueue_losses": 0,
                }
            )
            return redirect("profile") 
    else:
        form = RegisterSummonerForm()
        return render(request, 'register-summoner.html', {'form': form})

def get_summoner_info_register(request):
    gamename = request.GET.get('gamename')
    tagline = request.GET.get('tagline')

    summoner_registered = Invocador.objects.filter(nome_invocador=gamename,tag=tagline)
    if summoner_registered:
        return JsonResponse({'summoner': None,
                             'status_code': 405})
    riot_api = RiotAPI()
    data_puuid = riot_api.search_puuid_by_gamename(gamename, tagline)

    if data_puuid['status_code'] == 200:
        data_summoner = riot_api.search_summoner_data(data_puuid['puuid'])
        summoner = {'gamename': gamename,
                    'tagline': tagline,
                    'puuid': data_puuid['puuid'],
                    'summonerID': data_summoner['summonerID'],
                    'iconID': data_summoner['iconID'],
                    'summonerLevel': data_summoner['summonerLevel']}
        
        return JsonResponse({'summoner': summoner,
                             'status_code': data_summoner['status_code'],
                             'data_result': render_to_string("summoner-modal-result.html", {'summoner': summoner, 'current_patch': riot_api.patch })})

    else:
        return JsonResponse({'summoner': None,
                             'status_code': data_puuid['status_code']})

@login_required
@profile_user_data
def profile(request, context_dict):
    tier_data = get_object_or_404(Ranks, summoner=request.user.invocador.id)
    context_dict['tiers'] = tier_data

    # Paginação dos matches
    matches_list = Matches.objects.filter(summoner=request.user.invocador.id).order_by('-date')
    paginator = Paginator(matches_list, 10)
    page = request.GET.get('page', 1)

    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        matches = paginator.page(1)
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)

    # Processamento dos dados dos matches
    matches_data = [SummonerMatch(match.matchID, request.user.invocador.puuid) for match in matches]
    context_dict['matches'] = matches_data
    context_dict['page_obj'] = matches

    # Bloqueio de atualização
    last_update = request.user.invocador.last_updated_profile
    if last_update:
        context_dict['block_refresh'] = (timezone.now() - last_update) <= timedelta(minutes=2)
    else:
        context_dict['block_refresh'] = False

    # Teste de Hash
    data = "joaobreno"
    context_dict['hash_value'] = hashlib.sha256(data.encode()).hexdigest()

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


def refresh_summoner(request):
    if settings.CELERY_ASYNC_FUNCTIONS_DEBUG:
        task_refresh_summoner_async.delay(request.GET.get('id'))
    else:
        task_refresh_summoner_async(request.GET.get('id'))
    return JsonResponse({'response': datetime.datetime.now()})

def general_update_elo(request):
    if settings.CELERY_ASYNC_FUNCTIONS_DEBUG:
        task_update_many_summoner_async.delay()
    else:
        task_update_many_summoner_async()
    return JsonResponse({'response': True})


class SummonerMatch:
    def __init__(self, match_id, puuid):
        match = get_object_or_404(Matches, matchID=match_id)
        data = json.loads(match.data_json)
        blue_side_participants = []
        red_side_participants = []
        for index, participant in enumerate(data['info']['participants']):
            participant = self.correction_api_gg_endpoints(participant)
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
                self.remakeStatus = participant['gameEndedInEarlySurrender']
                if self.teamID == 100:
                    self.mainResult = data['info']['teams'][0]['win']
                elif self.teamID == 200:
                    self.mainResult = data['info']['teams'][1]['win']

        self.blue_side = {'participants': blue_side_participants, 'data': data['info']['teams'][0]}
        self.red_side = {'participants': red_side_participants, 'data': data['info']['teams'][1]}
        self.gameStartTime = datetime.datetime.fromtimestamp(data['info']['gameStartTimestamp'] / 1000.0)
        self.gameEndTime = datetime.datetime.fromtimestamp(data['info']['gameEndTimestamp'] / 1000.0)
        self.gameDuration = data['info']['gameDuration']
        self.queueId = data['info']['queueId']
        self.id = match.id
        self.matchPatch = match.gameVersion


    def str_gameDuration(self):
        minutes = self.gameDuration // 60
        seconds = self.gameDuration % 60
        return f"{minutes}:{seconds:02d}"
    
    def str_match_timeago(self):
        time_elapsed = datetime.datetime.now() - self.gameEndTime

        if time_elapsed.days >= 1:
            return f"{time_elapsed.days} {'dia' if time_elapsed.days == 1 else 'dias'}"
        elif time_elapsed.seconds >= 3600:
            hours = time_elapsed.seconds // 3600
            return f"{hours} {'hora' if hours == 1 else 'horas'}"
        else:
            minutes = time_elapsed.seconds // 60
            return f"{minutes} {'minuto' if minutes == 1 else 'minutos'}"
    
    def str_gameResult(self):
        if not self.remakeStatus:
            return 'Vitória' if self.mainResult else 'Derrota'
        else:
            return 'Remake'
    
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
        kda_ratio = (self.mainKDA['kills'] + self.mainKDA['assists']) / (self.mainKDA['deaths'] if self.mainKDA['deaths'] != 0 else 1)
        return '{:.2f}'.format(kda_ratio)

    def kill_presence(self):
        team = self.blue_side if self.teamID == 100 else self.red_side
        kp = ((self.mainKDA['kills'] + self.mainKDA['assists']) / (team['data']['objectives']['champion']['kills'] if team['data']['objectives']['champion']['kills'] != 0 else 1)) * 100
        return '{:.0f}%'.format(kp)
    
    def total_cs_qty(self):
        cs = self.mainSummoner['totalMinionsKilled'] + self.mainSummoner['neutralMinionsKilled']
        return '{:.0f}'.format(cs)

    def cs_per_minute(self):
        time = self.gameEndTime - self.gameStartTime
        cs = int(self.total_cs_qty()) / (time.seconds / 60)
        return '{:.1f}'.format(cs)
    
    def patch_media(self):
        correction = self.matchPatch.split('.')
        matchPatchVersion = f"{correction[0]}.{correction[1]}.1"
        return matchPatchVersion

    def correction_api_gg_endpoints(self, data):
        if data['championName'] == 'FiddleSticks':
            data['championName'] = 'Fiddlesticks'
        return data


@shared_task(name="task_refresh_summoner_async", bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 0, 'countdown': 120})
def task_refresh_summoner_async(self, summoner_id):
    server_settings = AdminSet.objects.all().first()
    summoner = Invocador.objects.get(pk=int(summoner_id))
    summoner.last_updated_profile = datetime.datetime.now()
    summoner.save()

    if server_settings.status_key:
        print('REFRESH MANUAL ====> {0}'.format(summoner.nome_invocador))

        riot_api = RiotAPI()
        status_user_name = riot_api.update_summoner_name_data(summoner.puuid)
        status_user_data = riot_api.update_summoner_data(summoner.puuid)
        status_solo_matches = riot_api.get_summoners_ranked_matches(summoner.puuid, Queue.SOLO.value)
        status_flex_matches = riot_api.get_summoners_ranked_matches(summoner.puuid, Queue.FLEX.value)
        status_elo_ranked = riot_api.update_summoner_elo_ranked_data(summoner.summonerId)
    
    
@shared_task(name="task_update_many_summoner_async", bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 0, 'countdown': 120})
def task_update_many_summoner_async(self):
    server_settings = AdminSet.objects.all().first()
    user_summoners = Invocador.objects.all()
    phantom_summoners = PhantomRanks.objects.all()

    if server_settings.status_key:
        qty = _log_console_title_section('UPDATE ELO GERAL')
        riot_api = RiotAPI()
        for user in user_summoners:
            status_elo_ranked = riot_api.update_summoner_elo_ranked_data(user.summonerId)
            _log_console_item_section(qty)
        for phantom in phantom_summoners:
            data_response = riot_api.get_summoner_data(phantom.puuid)
            if data_response['result']:
                phantom.summonerName = data_response['data']['summonerName']
                phantom.save()
            data_response = riot_api.search_summoner_data(phantom.puuid)
            if data_response['iconID']:
                phantom.profile_icon = data_response['iconID']
                phantom.save()
            data_result = riot_api.get_elo_ranked_data(phantom.summonerId)
            if data_result['result']:
                solo = data_result['SOLO_DATA']
                flex = data_result['FLEX_DATA']
                phantom.soloqueue_tier = solo['tier']
                phantom.flexqueue_tier = flex['tier']
                phantom.soloqueue_rank = solo['rank']
                phantom.flexqueue_rank = flex['rank']
                phantom.soloqueue_leaguePoints = solo['leaguePoints']
                phantom.flexqueue_leaguePoints = flex['leaguePoints']
                phantom.soloqueue_wins = solo['wins']
                phantom.flexqueue_wins = flex['wins']
                phantom.soloqueue_losses = solo['losses']
                phantom.flexqueue_losses = flex['losses']
                phantom.save()
                print("{0} PHANTOM updated".format(phantom.summonerName))
            _log_console_item_section(qty)
        qty = _log_console_title_section('FIM UPDATE')