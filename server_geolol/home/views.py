from django.shortcuts import render
from django.urls import *
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm
# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            redirect_url = reverse('login')
            return HttpResponseRedirect(redirect_url)
    else:        
        form = LoginForm()
    context_dict = {'form': form}
    return render(request, 'login.html', context=context_dict)