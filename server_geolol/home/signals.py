from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from datetime import date
from charts.models import LoginHistory

@receiver(user_logged_in)
def track_user_login(sender, request, user, **kwargs):
    if not LoginHistory.objects.filter(user=user, login_date=date.today()).exists():
        LoginHistory.objects.create(user=user, login_date=date.today())
        print("Login de {0} em {1}".format(user, date.today()))
