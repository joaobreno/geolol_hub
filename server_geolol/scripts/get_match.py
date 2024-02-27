from home.models import *
import requests
import datetime


matchID = 'BR1_2891213898'
key = 'RGAPI-6a7b9ebd-674a-4f54-8ff8-236589013e6b'
url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{matchID}?api_key={key}'

response = requests.get(url)

if response.status_code == 200:
    match_info = response.json()

    summoner = Invocador.objects.get(id=1)
    print(summoner)

    # match = Matches()
    # match.summoner = summoner
    # match.matchID="BR1_2891213898"
    # match.date=datetime.now()
    # match.gameMode=match_info['info']['gameMode']
    # match.gameVersion=match_info['info']['gameVersion']
    # match.summoner = summoner

    # match.save()

    # match.summoner.add(summoner)
    # match.save()

    match = Matches.objects.create(
        matchID=matchID,
        data_json = response.text,
        date=datetime.datetime.fromtimestamp(match_info['info']['gameEndTimestamp'] / 1000.0),
        gameMode=match_info['info']['gameMode'],
        gameVersion=match_info['info']['gameVersion']
    )

    # Adicione o Invocador à partida usando o método add()
    match.summoner.add(summoner)

print('ok')