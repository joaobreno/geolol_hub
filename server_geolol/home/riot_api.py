import requests
from riot_admin.models import AdminSet
from collections import defaultdict
from .models import *
from .utils import _log_console_title_section, _log_console_item_section
from charts.models import DiaryRank
from .enums import *
import pytz
import datetime
import time
import json


class RiotAPI():
    def __init__(self):
        server_settings = AdminSet.objects.all().first()
        self.api_key = server_settings.riot_api_key
        self.patch = server_settings.current_patch
        self.settings = server_settings
        self.queue_types = {420: 'SOLO', 440: 'FLEX'}

    def _decorator_exception(func):
        def _decorated(self, *args, **kwargs):
            try:
                return func(self,  *args, **kwargs)

            except requests.exceptions.RequestException as err:
                print ("Ops: Something Else",err)
                return False, err
            except requests.exceptions.HTTPError as errh:
                print ("Http Error:",errh)
                return False, errh
            except requests.exceptions.ConnectionError as errc:
                print ("Error Connecting:",errc)
                return False, errc
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt)
                return False, errt

        return _decorated
    
    def check_status_key(self, response):
        if response.status_code == 200:
            return True
        if response.status_code == 403 and self.settings.status_key:
            self.settings.status_key = False
            self.settings.save()
        print(response.text) if response.status_code != 403 else None
        return False
    
    
    def update_summoner_name_data(self, puuid):
        base_url = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}'

        params = {"api_key": self.api_key}

        response = requests.get(base_url, params=params)
        proceed = self.check_status_key(response)

        if proceed:
            data = response.json()
            summoner = Invocador.objects.get(puuid=puuid)
            summoner.nome_invocador = data['gameName']
            summoner.tag = data['tagLine']
            summoner.save()
        
        return proceed

    
    def get_summoners_ranked_matches(self, puuid, queue):
        summoner = Invocador.objects.get(puuid=puuid)
        season = Season.objects.filter(actual=True).first()

        start_time = season.start_time_unix()

        sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
        now_saopaulo = datetime.datetime.now(sao_paulo_tz)
        end_time = datetime_to_unix(now_saopaulo)

        base_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'

        # Iterar semanalmente
        current_time = start_time
        one_week = 7 * 24 * 60 * 60  # 1 semana em segundos

        qty = _log_console_title_section('REQUISIÇÕES DE PARTIDAS {0}'.format(self.queue_types.get(queue, 'SEM IDENTIFICAÇÃO')))
        while current_time < end_time:
            next_time = min(current_time + one_week, end_time)

            params = {
                "api_key": self.api_key,
                "startTime": current_time,
                "endTime": next_time,
                "queue": queue,
                "count": 100
            }

            response = requests.get(base_url, params=params)
            time.sleep(2)
            proceed = self.check_status_key(response)

            if proceed:
                data = response.json()
                print('|| TIME GAP ({0} - {1}) ||'.format(
                    datetime.datetime.fromtimestamp(current_time, sao_paulo_tz),
                    datetime.datetime.fromtimestamp(next_time, sao_paulo_tz)
                ))

                for matchID in data:
                    match_lib = Matches.objects.filter(matchID=matchID)
                    if not match_lib:
                        match_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchID}?api_key={self.api_key}'
                        match_response = requests.get(match_url)
                        time.sleep(0.5)
                        if match_response.status_code == 200:
                            print('{0} request status={1}'.format(matchID, match_response.status_code))
                            match_info = match_response.json()

                            match = Matches.objects.create(
                                matchID=matchID,
                                data_json=match_response.text,
                                date=datetime.datetime.fromtimestamp(match_info['info']['gameEndTimestamp'] / 1000.0),
                                gameMode=match_info['info']['gameMode'],
                                gameVersion=match_info['info']['gameVersion'],
                                queueType=match_info['info']['queueId'],
                                matchFinish=match_info['info']['participants'][0]['gameEndedInEarlySurrender'],
                                gameDuration=match_info['info']['gameDuration'],
                                season=season
                            )

                            match.summoner.add(summoner)
                    else:
                        print('{0} already registered'.format(matchID))
                        match = match_lib.first()
                        match.summoner.add(summoner)

                    summoner_match_data_lib = SummonerDataMatch.objects.filter(match=match,summoner=summoner)
                    if not summoner_match_data_lib:
                        data = json.loads(match.data_json)
                        user_target = None
                        for index, participant in enumerate(data['info']['participants']):
                            if participant['puuid'] == summoner.puuid:
                                user_target = participant
                                break
                        if user_target:
                            data_summoner_match = SummonerDataMatch.objects.create(
                                summoner=summoner,
                                riotIdGameName=user_target['riotIdGameName'],
                                match=match,
                                matchResult=('win' if user_target['win'] else 'lose'),
                                gameEndedInSurrender=user_target['gameEndedInSurrender'],
                                remake=user_target['gameEndedInEarlySurrender'],
                                championID=user_target['championId'],
                                championName=user_target['championName'],
                                championLevel=user_target['champLevel'],
                                kills=user_target['kills'],
                                deaths=user_target['deaths'],
                                assists=user_target['assists'],
                                kda=user_target['challenges']['kda'],
                                teamPosition=user_target['lane'],
                                timePlayed=user_target['timePlayed'],
                                item0=user_target['item0'],
                                item1=user_target['item1'],
                                item2=user_target['item2'],
                                item3=user_target['item3'],
                                item4=user_target['item4'],
                                item5=user_target['item5'],
                                item6=user_target['item6'],
                                doubleKills=user_target['doubleKills'],
                                tripleKills=user_target['tripleKills'],
                                quadraKills=user_target['quadraKills'],
                                pentaKills=user_target['pentaKills'],
                                firstBloodKill=user_target['firstBloodKill'],
                                firstTowerKill=user_target['firstTowerKill'],
                                largestKillingSpree=user_target['largestKillingSpree'],
                                largestMultiKill=user_target['largestMultiKill'],
                                bountyLevel=user_target['bountyLevel'],
                                quickSoloKills=user_target['challenges']['quickSoloKills'],
                                killParticipation=user_target['challenges'].get('killParticipation', 0),
                                damageDealtToBuildings=user_target['damageDealtToBuildings'],
                                damageDealtToObjectives=user_target['damageDealtToObjectives'],
                                damageDealtToTurrets=user_target['damageDealtToTurrets'],
                                damageSelfMitigated=user_target['damageSelfMitigated'],
                                totalDamageShieldedOnTeammates=user_target['totalDamageShieldedOnTeammates'],
                                totalHeal=user_target['totalHeal'],
                                totalHealsOnTeammates=user_target['totalHealsOnTeammates'],
                                physicalDamageDealtToChampions=user_target['physicalDamageDealtToChampions'],
                                magicDamageDealtToChampions=user_target['magicDamageDealtToChampions'],
                                totalDamageDealt=user_target['totalDamageDealt'],
                                totalDamageDealtToChampions=user_target['totalDamageDealtToChampions'],
                                totalDamageTaken=user_target['totalDamageTaken'],
                                goldEarned=user_target['goldEarned'],
                                CS=(user_target['totalMinionsKilled']+user_target['neutralMinionsKilled']),
                                objectivesStolen=user_target['objectivesStolen'],
                                turretKills=user_target['turretKills'],
                                dragonTakedowns=user_target['challenges']['dragonTakedowns'],
                                teamBaronKills=user_target['challenges']['teamBaronKills'],
                                visionScore=user_target['visionScore'],
                                visionWardsBoughtInGame=user_target['visionWardsBoughtInGame'],
                                wardsKilled=user_target['wardsKilled'],
                                wardsPlaced=user_target['wardsPlaced'],
                                detectorWardsPlaced=user_target['detectorWardsPlaced'],
                                visionScorePerMinute=user_target['challenges']['visionScorePerMinute'],
                                skillshotsDodged=user_target['challenges']['skillshotsDodged'],
                                skillshotsHit=user_target['challenges']['skillshotsHit'],
                                timeCCingOthers=user_target['timeCCingOthers'],
                                QSpellCasts=user_target['spell1Casts'],
                                WSpellCasts=user_target['spell2Casts'],
                                ESpellCasts=user_target['spell3Casts'],
                                UltSpellCasts=user_target['spell4Casts'],
                                totalTimeSpentDead=user_target['totalTimeSpentDead'],
                                longestTimeSpentLiving=user_target['longestTimeSpentLiving']
                            )

                    else:
                        data_summoner_match = summoner_match_data_lib.first()
                        print('DATA MATCH => {0} ({1} - {2}/{3}/{4}) already saved.'.format(data_summoner_match.riotIdGameName,
                                                                                            data_summoner_match.championName,
                                                                                            data_summoner_match.kills,
                                                                                            data_summoner_match.deaths,
                                                                                            data_summoner_match.assists))
                _log_console_item_section(qty)

            else:
                print(f"Erro na requisição: {response.status_code}")
            current_time = next_time

        qty = _log_console_title_section('FIM DE REQUISIÇÕES')
        return proceed


    def search_puuid_by_gamename(self, gameName, tagLine):
        base_url = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}'

        params = {"api_key": self.api_key}

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            puuid = data['puuid']
        else:
            puuid =  None

        return {'puuid': puuid, 'status_code': response.status_code}
        
    
    def search_summoner_data(self, puuid):
        base_url = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}'

        params = {"api_key": self.api_key}

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data_response = response.json()
            data = {
                'summonerID': data_response['id'],
                'iconID': data_response['profileIconId'],
                'summonerLevel': data_response['summonerLevel'],
                'status_code': response.status_code
            }
        else:
            data = {
                'summonerID': None,
                'iconID': None,
                'summonerLevel': None,
                'status_code': response.status_code
            }

        return data
    
    def update_summoner_data(self, puuid):
        summoner = Invocador.objects.get(puuid=puuid)
        base_url = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}'

        params = {"api_key": self.api_key}

        response = requests.get(base_url, params=params)
        proceed = self.check_status_key(response)

        if proceed:
            data = response.json()
            summoner.profile_icon = data['profileIconId']
            summoner.level = data['summonerLevel']
            summoner.save()

        return proceed
    
    def update_summoner_elo_ranked_data(self, summonerID):
        rank = Ranks.objects.get(summoner__summonerId=summonerID)
        base_url = f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerID}'

        params = {"api_key": self.api_key}

        response = requests.get(base_url, params=params)
        proceed = self.check_status_key(response)

        if proceed:
            #TODO UPDATE ELO DOS USUARIOS
            data = response.json()
            solo_queue = next((item for item in data if item['queueType'] == 'RANKED_SOLO_5x5'), None)
            flex_queue = next((item for item in data if item['queueType'] == 'RANKED_FLEX_SR'), None)

            rank.soloqueue_tier = solo_queue.get('tier', 'UNRANKED') if solo_queue else 'UNRANKED'
            rank.soloqueue_rank = solo_queue.get('rank', '') if solo_queue else ''
            rank.soloqueue_leaguePoints = solo_queue.get('leaguePoints', 0) if solo_queue else 0
            rank.soloqueue_wins = solo_queue.get('wins', 0) if solo_queue else 0
            rank.soloqueue_losses = solo_queue.get('losses', 0) if solo_queue else 0
            rank.flexqueue_tier = flex_queue.get('tier', 'UNRANKED') if flex_queue else 'UNRANKED'
            rank.flexqueue_rank = flex_queue.get('rank', '') if flex_queue else ''
            rank.flexqueue_leaguePoints = flex_queue.get('leaguePoints', 0) if flex_queue else 0
            rank.flexqueue_wins = flex_queue.get('wins', 0) if flex_queue else 0
            rank.flexqueue_losses = flex_queue.get('losses', 0) if flex_queue else 0
            rank.save()

            season = Season.objects.filter(actual=True).first()
            sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
            date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=sao_paulo_tz)
            diary, diary_created = DiaryRank.objects.get_or_create(
                summoner=rank.summoner,
                season=season,
                date=date,
                defaults={
                    'soloqueue_tier': solo_queue.get('tier', 'UNRANKED') if solo_queue else 'UNRANKED',
                    'flexqueue_tier': flex_queue.get('tier', 'UNRANKED') if flex_queue else 'UNRANKED',
                    'soloqueue_rank': solo_queue.get('rank', '') if solo_queue else '',
                    'flexqueue_rank': flex_queue.get('rank', '') if flex_queue else '',
                    'soloqueue_leaguePoints': solo_queue.get('leaguePoints', 0) if solo_queue else 0,
                    'flexqueue_leaguePoints': flex_queue.get('leaguePoints', 0) if flex_queue else 0,
                    'soloqueue_wins': solo_queue.get('wins', 0) if solo_queue else 0,
                    'flexqueue_wins': flex_queue.get('wins', 0) if flex_queue else 0,
                    'soloqueue_losses': solo_queue.get('losses', 0) if solo_queue else 0,
                    'flexqueue_losses': flex_queue.get('losses', 0) if flex_queue else 0,
                }
            )

            if diary_created:
                print('{0} Diary created successfully!'.format(rank.summoner.nome_invocador))
            else:
                diary.soloqueue_tier = solo_queue.get('tier', 'UNRANKED') if solo_queue else 'UNRANKED'
                diary.flexqueue_tier = flex_queue.get('tier', 'UNRANKED') if flex_queue else 'UNRANKED'
                diary.soloqueue_rank = solo_queue.get('rank', '') if solo_queue else ''
                diary.flexqueue_rank = flex_queue.get('rank', '') if flex_queue else ''
                diary.soloqueue_leaguePoints = solo_queue.get('leaguePoints', 0) if solo_queue else 0
                diary.flexqueue_leaguePoints = flex_queue.get('leaguePoints', 0) if flex_queue else 0
                diary.soloqueue_wins = solo_queue.get('wins', 0) if solo_queue else 0
                diary.flexqueue_wins = flex_queue.get('wins', 0) if flex_queue else 0
                diary.soloqueue_losses = solo_queue.get('losses', 0) if solo_queue else 0
                diary.flexqueue_losses = flex_queue.get('losses', 0) if flex_queue else 0
                diary.save()
                print('{0} Diary updated successfully!'.format(rank.summoner.nome_invocador))


        return proceed
    

    def get_summoner_data(self, puuid):
        base_url = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}'
        params = {"api_key": self.api_key}

        data_result = {'result': False, 'data': {}}

        try:
            response = requests.get(base_url, params=params)

            if not self.check_status_key(response):
                data_result['data'] = {
                    'summonerName': None,
                    'tagLine': None,
                    'status_code': response.status_code
                }
                return data_result  
            
            data_response = response.json()
            data_result['result'] = True
            data_result['data'] = {
                'summonerName': data_response.get('gameName'),
                'tagLine': data_response.get('tagLine'),
                'status_code': response.status_code
            }

        except requests.exceptions.RequestException as e:
            # Captura erros de requisição (conexão, timeout, etc.)
            data_result['data'] = {
                'summonerName': None,
                'tagLine': None,
                'status_code': None,
                'error': str(e)
            }

        return data_result

    
    def get_elo_ranked_data(self, summonerID):
        base_url = f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerID}'
        params = {"api_key": self.api_key}

        response = requests.get(base_url, params=params)
        if not self.check_status_key(response):
            return {'result': False, 'SOLO_DATA': {}, 'FLEX_DATA': {}}

        ranked_data = response.json() or []
        data = defaultdict(dict)
        data['result'] = True

        def extract_ranked_data(queue_type):
            queue = next((item for item in ranked_data if item['queueType'] == queue_type), {})
            return {
                'tier': queue.get('tier', 'UNRANKED'),
                'rank': queue.get('rank', ''),
                'leaguePoints': queue.get('leaguePoints', 0),
                'wins': queue.get('wins', 0),
                'losses': queue.get('losses', 0),
            }

        data['SOLO_DATA'] = extract_ranked_data('RANKED_SOLO_5x5')
        data['FLEX_DATA'] = extract_ranked_data('RANKED_FLEX_SR')

        return dict(data)