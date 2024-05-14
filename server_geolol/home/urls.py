from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/profile/', views.profile, name='profile'),
    path('home/profile/refresh_summoner', views.refresh_summoner, name='profile-refresh'),
]