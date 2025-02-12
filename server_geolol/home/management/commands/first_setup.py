from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Invocador, Ranks, Season
from riot_admin.models import AdminSet
from django.utils import timezone
from pytz import timezone as pytz_timezone

class Command(BaseCommand):
    help = 'Cria um usuário, invocador, rank e AdminSet se não existirem.'

    def handle(self, *args, **kwargs):
        # Verifica se o usuário já existe
        user, created = User.objects.get_or_create(
            username='joaobreno',
            defaults={
                'is_superuser': True,
                'is_staff': True,
            }
        )

        # Se o usuário foi criado, define a senha
        if created:
            user.set_password('18061995')
            user.save()
            self.stdout.write(self.style.SUCCESS('Usuário criado com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING('Usuário já existia.'))

        # Verifica se já existe um Invocador para esse usuário
        invocador, invocador_created = Invocador.objects.get_or_create(
            user=user,
            defaults={
                'nome_invocador': 'CLTT',
                'tag': 'GEO',
                'profile_icon': '512',
                'puuid': '05DFZz6OhwJxj20Oqks3YHgE0ZW4BMtmQ4bVkapPcwk5e7yQasKIKd0HSZZPgOkkCPuK5sZlecgOFQ',
                'summonerId': '1VGy4IH2X3gpLXXpimRydF80JCipMVurCc0w80Jld2yZ7w',
                'level': 675,
            }
        )

        if invocador_created:
            self.stdout.write(self.style.SUCCESS('Invocador criado com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING('Invocador já existia.'))

        # Verifica se já existe um Rank para esse Invocador
        rank, rank_created = Ranks.objects.get_or_create(
            summoner=invocador,
            defaults={
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
            self.stdout.write(self.style.SUCCESS('Rank criado com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING('Rank já existia.'))

        # Verifica se já existe um AdminSet
        admin_set, admin_set_created = AdminSet.objects.get_or_create(
            defaults={
                'riot_api_key': 'RGAPI-b1c05913-00d9-4aa0-8f83-6f6e098f6a55',
                'status_key': True,
            }
        )

        if admin_set_created:
            self.stdout.write(self.style.SUCCESS('AdminSet criado com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING('AdminSet já existia.'))

        
         # Verifica se já existe uma Season
        sao_paulo_tz = pytz_timezone('America/Sao_Paulo')
        start_time = timezone.datetime(2025, 1, 9, 9, 0, tzinfo=sao_paulo_tz)

        season, season_created = Season.objects.get_or_create(
            name='Temporada 2025.1',
            defaults={
                'description': '',
                'startTime': start_time,
                'actual': True,
            }
        )

        if season_created:
            self.stdout.write(self.style.SUCCESS('Season criada com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING('Season já existia.'))