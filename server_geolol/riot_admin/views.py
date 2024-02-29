from django.shortcuts import render, redirect, get_object_or_404
from django.urls import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings 
import requests
from home.decorator import *
from .models import *
from .models import *
# Create your views here.

@login_required
def server_settings(request):
    return render(request, 'index.html')