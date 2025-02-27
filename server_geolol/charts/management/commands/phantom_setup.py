from django.core.management.base import BaseCommand
from home.models import Invocador
from home.riot_api import *
from charts.models import PhantomRanks


class Command(BaseCommand):
    help = 'Cria usuários default para aparecer em Leaderboards. Caso exista Usuários, serão deletados.'

    def handle(self, *args, **kwargs):
        geolol_group = [
            {
                'gameName': 'CLTT',
                'puuid': '05DFZz6OhwJxj20Oqks3YHgE0ZW4BMtmQ4bVkapPcwk5e7yQasKIKd0HSZZPgOkkCPuK5sZlecgOFQ',
                'id': '1VGy4IH2X3gpLXXpimRydF80JCipMVurCc0w80Jld2yZ7w'
            },

            {
                'gameName': 'Embaixador 2026',
                'puuid': '3b30SCBKPrf4QW0ubUG83Rkg2b2M75ToN6toD_pWVt4D6jK4EZ7UY2E4Tv2XIdsNzrC37QZcVfEpAA',
                'id': '85zUdozL1KkP4xKLBJwfRe9SFIwAU6YaF5zSZaxT8wFY'
            },
            {
                'gameName': 'Little Vitu',
                'puuid': 'RyOUDE73D1pb9E7Ea-eNcyqZihBm29zR3NifohXP_utZuy7HE_-LNzBXPqnGkKXkma8BFsTaqf7Jwg',
                'id': 'cEtR53UVy8njk87YamHaR7UBEMTZnmgDInEkGmnjrL9c_eY'
            },
            {
                'gameName': 'saci de 2 perna',
                'puuid': 'Mr0SjF_EzBBldFTirqSNWjrOqLxbhyTsMRAzEyEyYD1uZBxAKQ5fum0vLJxq6omuzSPtUHQiX6TgIg',
                'id': '3Dpav4iMQI4sIZ3Cyc4O04YKh2JrYjf3jW2YPH1SvcVheGs'
            },
            {
                'gameName': 'Kagaro Nakama',
                'puuid': 'LBam-Zj-StYxj4q9Ku8jz5XiA7hzf1nTE-SFiLqUhsGOG8yiiQ3kyv53LHl1WwXuJQd4u9odB-xOWg',
                'id': '2TBW6scQM0oumLdG5RDkwKC6rw-Vz8EhBd_KWf3TrwQAsg'
            },
            {
                'gameName': 'Pâmela Confete',
                'puuid': 'xfJEzq6OGyL2GVmA3A1nFDSNQ4o7coOsjUIVNZXfQcz5v4WY5scd2a9Kq24i5qZ2OpZtZW8IMWgniQ',
                'id': '6AJShbKMbk8Ymaj7w5xYX2wPq2CIrW_ue8ytnmpJDlXDXg'
            },
            {
                'gameName': 'FrangoTorto',
                'puuid': 'uLVthA2TpD6NhpNFjxwDoqVf0-ubF5vrWXvLyLlh7qgxcQ18F1R94--jjighHgqz_bgVf8gyIhtOjw',
                'id': 'p0XVTe0I91L5-Gap02C7vE2COz8B-juE7jx9a8G91s9h7g'
            },
            {
                'gameName': 'Arenito Killer',
                'puuid': 'nhmk54JBp4wC5MHhO_OHkHBhA5u5TDKgifQr84ssgePYT9bgMwlu8Fe52N_RCXp-XAWl4aRmgpsUkA',
                'id': '5YxH-ir0KqAV93QiaWxOm5PuRM8V1dboOB15dZ9lieQSxg'
            },
            {
                'gameName': 'SHAKAZIN',
                'puuid': 'beXO2EH9xo7lbxBH3X4TgTn3GG26Zr_E38rS2sWQnUQEIejuCo7I44OnZPseWX7M_X4G4lqCjyiSBA',
                'id': 'ViwvFx18ZNDL7YZSMe648fZdqg_ppU3j400kX5DjsZnGeq8'
            },
            {
                'gameName': 'Offering',
                'puuid': 'GGY8UmZC7d1PbQViY1ntqWl7TJftS0NGYga5jRkXlJtVrzyFvgn1DEo6dBiiqoQBNgnw3gE9UrhXyQ',
                'id': 'L82eZcTpXmg7uw3RYocVW_HHc5fsds0RvqU1OEVfih7EG5A'
            },
            {
                'gameName': 'valter',
                'puuid': 'InPfYcmePmmOFOrqn4PrWblj25wdsUPPyMgcXnUqdawFHk3X1ewUVeYLDoYH77apHUHBgV-4h1qzmQ',
                'id': 'Av42ILPtw1T6djBtpKHWonezCNfFAUErhlobIlQupz9lOQ'
            },
            {
                'gameName': 'Jc1n',
                'puuid': 'N0eagOnfRpMrBEC9UijlHDSLVB4hs1IVD-E996dh0lsaTCpe-tnfYn4-3JOiJTCCy5DqGxmpDbCerA',
                'id': 'Jied0ku3-DNpUKRXB2L1W090lZKQZRNUynqoBwiSDY91LA'
            },
            {
                'gameName': 'PR0tozo4rio',
                'puuid': 'ziBwipjIwAjjRFHYvrKDK0Ma9JNcgM1Ui649YRk0J0zyQbUfVWQKWe_93ID8H5fmnh1A7X1YmAH2eg',
                'id': 'PaeA5VebRYUDG1QigQWXPIirIAggEMI44SV7qcNzCATkUwI'
            },
            {
                'gameName': 'Freitax',
                'puuid': '0D0BuUeiJ8njxijc8uf1oac54ANGSQMsG5BTZq-BKQryJgB98OKjQUuCHOMw9UV_zoyV1ocyGqHmlg',
                'id': 'Cr4T-oLZraop6RwkeLTq5kVZsMlE5KF6LGo7fSlqRhS0Nw'
            },
        ]

        for default_user in geolol_group:
            try:
                summoner = Invocador.objects.get(puuid=default_user['puuid'])
                self.stdout.write(self.style.WARNING('Summoner {0} já cadastrado no sistema.'.format(summoner.nome_invocador)))
            except Invocador.DoesNotExist:
                summoner = None
            
            if not summoner:
                rank, rank_created = PhantomRanks.objects.get_or_create(
                    puuid=default_user['puuid'],
                    defaults={
                        'summonerName': default_user['gameName'],
                        'summonerId': default_user['id'],
                        'profile_icon': 512,
                        'soloqueue_tier': 'UNRANKED',
                        'flexqueue_tier': 'UNRANKED',
                        'soloqueue_rank': '',
                        'flexqueue_rank': '',
                        'soloqueue_leaguePoints': 0,
                        'flexqueue_leaguePoints': 0,
                        'soloqueue_wins': 0,
                        'flexqueue_wins': 0,
                        'soloqueue_losses': 0,
                        'flexqueue_losses': 0,
                    }
                )

                if rank_created:
                    self.stdout.write(self.style.SUCCESS('PhantomRank de {0} criado com sucesso!'.format(default_user['gameName'])))
                else:
                    self.stdout.write(self.style.WARNING('PhantomRank de {0} já existia.'.format(default_user['gameName'])))

                