from django.db import models
from django.contrib.auth.models import User
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
    # Adicione outros atributos conforme necessário

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
        return "{:.0f}%".format((self.soloqueue_wins / (self.soloqueue_losses + self.soloqueue_wins )) * 100)
    
    @property
    def flex_winrate(self):
        return "{:.0f}%".format((self.flexqueue_wins / (self.flexqueue_losses + self.flexqueue_wins )) * 100)
    
class Matches(models.Model):
    summoner = models.ManyToManyField(Invocador, related_name='+')

    matchID = models.CharField(max_length=20, blank=True)
    data_json = models.TextField(blank=True)
    date = models.DateTimeField(blank=True)
    gameMode = models.CharField(max_length=20, blank=True)
    gameVersion = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.matchID