import requests
from riot_admin.models import AdminSet
from .models import *
import datetime


class RiotAPI():
    def __init__(self):
        server_settings = AdminSet.objects.all().first()
        self.api_key = server_settings.riot_api_key

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
    
    def get_summoners_ranked_matches(self, puuid, queue):
        summoner = Invocador.objects.get(puuid=puuid)
        base_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'

        params = {
            "api_key": self.api_key,
            "startTime": 1704067200,
            "queue": queue
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            for matchID in data:
                match_lib = Matches.objects.filter(matchID=matchID)
                if not match_lib:
                    match_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchID}?api_key={self.api_key}'
                    match_response = requests.get(match_url)
                    if match_response.status_code == 200:
                        print('{0} request status={1}'.format(matchID, match_response.status_code))
                        match_info = match_response.json()

                        match = Matches.objects.create(
                            matchID=matchID,
                            data_json = match_response.text,
                            date=datetime.datetime.fromtimestamp(match_info['info']['gameEndTimestamp'] / 1000.0),
                            gameMode=match_info['info']['gameMode'],
                            gameVersion=match_info['info']['gameVersion']
                        )

                        # Adicione o Invocador à partida usando o método add()
                        match.summoner.add(summoner)
                else:
                    print('{0} already registered'.format(matchID))
                    match = match_lib.first()
                    match.summoner.add(summoner)
        else:
            print(f"Erro na requisição: {response.status_code}")