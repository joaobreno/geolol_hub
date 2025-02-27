from django.db import models

# Create your models here.
class PhantomRanks(models.Model):
    summonerName = models.CharField(max_length=50, blank=True)
    puuid = models.CharField(max_length=100, blank=True)
    summonerId = models.CharField(max_length=100, blank=True)
    profile_icon = models.CharField(max_length=10, blank=True)

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
        return "Phantom {0}".format(self.summonerName)
    
    @property
    def solo_rank_str(self):
        return "{0} {1}".format(self.soloqueue_tier, self.soloqueue_rank)
    
    @property
    def flex_rank_str(self):
        return "{0} {1}".format(self.flexqueue_tier, self.flexqueue_rank)
    
    @property
    def solo_lp_points_str(self):
        return "{0} LP".format(self.soloqueue_leaguePoints)
    
    @property
    def flex_lp_points_str(self):
        return "{0} LP".format(self.flexqueue_leaguePoints)

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