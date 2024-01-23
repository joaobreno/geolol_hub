from django.shortcuts import render
from django.urls import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required
def profile(request):
    return render(request, 'users-profile.html')