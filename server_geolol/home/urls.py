from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/profile/', views.profile, name='profile'),
    path('home/register-summoner', views.register_summoner, name='register-summoner'),
    path('home/profile/refresh_summoner', views.refresh_summoner, name='profile-refresh'),
    path('home/profile/refresh_summoner/get_info_request', views.get_summoner_info_register, name='get-summoner-info-request'),
]