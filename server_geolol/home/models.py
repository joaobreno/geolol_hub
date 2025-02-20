from django.db import models
from django.contrib.auth.models import User, AbstractUser
from .utils import *
# Create your models here.

class Invocador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_invocador = models.CharField(max_length=50, blank=True)
    tag = models.CharField(max_length=10, blank=True)
    profile_icon = models.CharField(max_length=10, blank=True)
    puuid = models.CharField(max_length=100, blank=True)
    summonerId = models.CharField(max_length=100, blank=True)
    level = models.IntegerField(blank=True, default=0)
    summonerName = models.CharField(max_length=50, blank=True)
    last_updated_profile = models.DateTimeField(blank=True, null=True)
    admin_authorized = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username
    

class Ranks(models.Model):
    summoner = models.ForeignKey(Invocador, on_delete=models.CASCADE)

    # RANKED_SOLO_5x5
    soloqueue_tier = models.CharField(max_length=20, blank=True)
    soloqueue_rank = models.CharField(max_length=5, blank=True)
    soloqueue_leaguePoints = models.IntegerField(blank=True)
    soloqueue_wins = models.IntegerField(blank=True)
    soloqueue_losses = models.IntegerField(blank=True)

    # RANKED_FLEX_SR
    flexqueue_tier = models.CharField(max_length=20, blank=True)
    flexqueue_rank = models.CharField(max_length=5, blank=True)
    flexqueue_leaguePoints = models.IntegerField(blank=True)
    flexqueue_wins = models.IntegerField(blank=True)
    flexqueue_losses = models.IntegerField(blank=True)

    def __str__(self):
        return self.summoner.user.username
    
    @property
    def solo_winrate(self):
        try:
            return "{:.0f}%".format((self.soloqueue_wins / (self.soloqueue_losses + self.soloqueue_wins )) * 100)
        except Exception as e:
            return "0%"
    
    @property
    def flex_winrate(self):
        try:
            return "{:.0f}%".format((self.flexqueue_wins / (self.flexqueue_losses + self.flexqueue_wins )) * 100)
        except Exception as e:
            return "0%"


class Season(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    startTime = models.DateTimeField(blank=True, null=True)
    actual = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def start_time_unix(self):
        return datetime_to_unix(self.startTime)


class Matches(models.Model):
    summoner = models.ManyToManyField(Invocador, related_name='+')

    matchID = models.CharField(max_length=20, blank=True)
    data_json = models.TextField(blank=True)
    date = models.DateTimeField(blank=True)
    gameMode = models.CharField(max_length=20, blank=True)
    gameVersion = models.CharField(max_length=20, blank=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.matchID