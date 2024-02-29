from django.urls import path, include
from . import views

urlpatterns = [
    path('serversettings/', views.server_settings, name='server-settings'),
]