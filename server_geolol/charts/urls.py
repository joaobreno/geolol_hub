from django.urls import path, include
from . import views

urlpatterns = [
    path('leaderboards/', views.leaderboards, name='leaderboards'),
]