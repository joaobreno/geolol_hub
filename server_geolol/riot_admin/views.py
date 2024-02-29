from django.shortcuts import render, redirect, get_object_or_404
from django.urls import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.conf import settings 
import requests
from home.decorator import *
from riot_admin.models import AdminSet
from .models import *
from .forms import *
# Create your views here.

@login_required
@profile_user_data
def server_settings(request, context_dict):
    admin_set = get_object_or_404(AdminSet, pk=1)   
    if request.method == 'POST':
        form = RiotAPIKeyForm(request.POST, admin=admin_set) 
        if form.is_valid():
            admin_set.riot_api_key = form.cleaned_data['api_key']
            admin_set.save()
            redirect_url = reverse('profile')
            return HttpResponseRedirect(redirect_url)
    else:
        form = RiotAPIKeyForm(admin=admin_set) 
        context_dict['form'] = form
    return render(request, 'server-settings-form.html', context_dict)