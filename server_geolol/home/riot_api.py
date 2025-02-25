import requests
from riot_admin.models import AdminSet
from .models import *
import pytz
import datetime
import time


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

        print('X=================== REQUISIÇÕES DE PARTIDAS {0} ===================X'.format(self.queue_types.get(queue, 'SEM IDENTIFICAÇÃO')))
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
                                season=season
                            )

                            match.summoner.add(summoner)
                    else:
                        print('{0} already registered'.format(matchID))
                        match = match_lib.first()
                        match.summoner.add(summoner)
                print('----------------------------------------------------------------------')

            else:
                print(f"Erro na requisição: {response.status_code}")
            current_time = next_time

        print('X======================== FIM DE REQUISIÇÕES ========================X\n')
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
            data = response.json()
            data = {
                'summonerID': data['id'],
                'iconID': data['profileIconId'],
                'summonerLevel': data['summonerLevel'],
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


        return proceed