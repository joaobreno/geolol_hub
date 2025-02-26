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
    queueType = models.IntegerField(blank=True, default=1)
    matchFinish = models.BooleanField(default=True)
    gameDuration = models.IntegerField(blank=True, default=0)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.matchID
    
class SummonerDataMatch(models.Model):
    summoner = models.ForeignKey(Invocador, related_name='matches_data', on_delete=models.CASCADE)
    riotIdGameName = models.CharField(max_length=30, blank=True)
    match = models.ForeignKey(Matches, related_name='summoners_related', on_delete=models.CASCADE)
    matchResult = models.CharField(max_length=10, blank=True)
    gameEndedInSurrender = models.BooleanField(default=False)
    remake = models.BooleanField(default=False)

    ### MATCH DATA
    championID = models.IntegerField(blank=True)
    championName = models.CharField(max_length=30, blank=True)
    championLevel = models.IntegerField(blank=True)
    kills = models.IntegerField(blank=True)
    deaths = models.IntegerField(blank=True)
    assists = models.IntegerField(blank=True)
    kda = models.DecimalField(max_digits=20, decimal_places=2)
    teamPosition = models.CharField(max_length=10, blank=True)
    timePlayed = models.IntegerField(blank=True)

    ### ITEMS
    item0 = models.IntegerField(blank=True)
    item1 = models.IntegerField(blank=True)
    item2 = models.IntegerField(blank=True)
    item3 = models.IntegerField(blank=True)
    item4 = models.IntegerField(blank=True)
    item5 = models.IntegerField(blank=True)
    item6 = models.IntegerField(blank=True)
    
    ### SCORE STATS
    doubleKills = models.IntegerField(blank=True)
    tripleKills = models.IntegerField(blank=True)
    quadraKills = models.IntegerField(blank=True)
    pentaKills = models.IntegerField(blank=True)
    firstBloodKill = models.BooleanField(default=False)
    firstTowerKill = models.BooleanField(default=False)
    largestKillingSpree = models.IntegerField(blank=True)
    largestMultiKill = models.IntegerField(blank=True)
    bountyLevel = models.IntegerField(blank=True)
    quickSoloKills = models.IntegerField(blank=True)
    killParticipation = models.DecimalField(max_digits=20, decimal_places=2)

    ### DAMAGE STATS
    damageDealtToBuildings = models.IntegerField(blank=True)
    damageDealtToObjectives = models.IntegerField(blank=True)
    damageDealtToTurrets = models.IntegerField(blank=True)
    damageSelfMitigated = models.IntegerField(blank=True)
    totalDamageShieldedOnTeammates = models.IntegerField(blank=True)
    totalHeal = models.IntegerField(blank=True)
    totalHealsOnTeammates = models.IntegerField(blank=True)
    physicalDamageDealtToChampions = models.IntegerField(blank=True)
    magicDamageDealtToChampions = models.IntegerField(blank=True)
    totalDamageDealt = models.IntegerField(blank=True)
    totalDamageDealtToChampions = models.IntegerField(blank=True)
    totalDamageTaken = models.IntegerField(blank=True)

    ### MAP STATS
    goldEarned = models.IntegerField(blank=True)
    CS = models.IntegerField(blank=True)
    objectivesStolen = models.IntegerField(blank=True)
    turretKills = models.IntegerField(blank=True)
    dragonTakedowns = models.IntegerField(blank=True)
    teamBaronKills = models.IntegerField(blank=True)

    ### VISION STATS
    visionScore = models.IntegerField(blank=True)
    visionWardsBoughtInGame = models.IntegerField(blank=True)
    wardsKilled = models.IntegerField(blank=True)
    wardsPlaced = models.IntegerField(blank=True)
    detectorWardsPlaced = models.IntegerField(blank=True)
    visionScorePerMinute = models.DecimalField(max_digits=20, decimal_places=2)

    ### OTHER STATS
    skillshotsDodged = models.IntegerField(blank=True)
    skillshotsHit = models.IntegerField(blank=True)
    timeCCingOthers = models.IntegerField(blank=True)
    QSpellCasts = models.IntegerField(blank=True)
    WSpellCasts = models.IntegerField(blank=True)
    ESpellCasts = models.IntegerField(blank=True)
    UltSpellCasts = models.IntegerField(blank=True)
    totalTimeSpentDead = models.IntegerField(blank=True)
    longestTimeSpentLiving = models.IntegerField(blank=True)
    

