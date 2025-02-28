from django.shortcuts import render
from home.decorator import *
from django.contrib.auth.decorators import login_required
from home.models import Invocador, Ranks
from charts.models import PhantomRanks
from django.db.models import F, Value, IntegerField

def custom_sort(conquest):
    tier_order = {'DIAMOND': 0, 'EMERALD': 1, 'PLATINUM': 2, 'GOLD': 3, 'SILVER': 4, 'BRONZE': 5, 'IRON': 6, 'UNRANKED': 7}
    rank_order = {'I': 0, 'II': 1, 'III': 2, 'IV': 3}

    tier = conquest['soloqueue_tier']
    rank = conquest['soloqueue_rank']

    return (tier_order.get(tier, len(tier_order)), rank_order.get(rank, len(rank_order)), -conquest['soloqueue_leaguePoints'])


@login_required
@profile_user_data
def leaderboards(request, context_dict):
    context_dict['main_class']= 'ranking-main'
    user_ranks = Ranks.objects.all().values(
        'soloqueue_tier',
        'soloqueue_rank',
        'soloqueue_leaguePoints',
        'summoner__nome_invocador'
    ).annotate(
        summonerName=F('summoner__nome_invocador')
    ).values(
        'soloqueue_tier',
        'soloqueue_rank',
        'soloqueue_leaguePoints',
        'summonerName'
    )

    phantom_ranks = PhantomRanks.objects.all().values(
        'soloqueue_tier',
        'soloqueue_rank',
        'soloqueue_leaguePoints',
        'summonerName'
    )
    combined_ranks = list(user_ranks.union(phantom_ranks))
    final_ranking = sorted(combined_ranks, key=custom_sort)
    for pos, player in enumerate(final_ranking, start=1):
        player['pos'] = pos
    context_dict['ranking'] = final_ranking[0:6]
    return render(request, 'leaderboards.html', context_dict)
