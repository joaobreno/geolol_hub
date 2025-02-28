from django.shortcuts import render, redirect, get_object_or_404
from riot_admin.models import *
from geolol_hub.settings import *
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from .models import Invocador

def profile_user_data(func):
    def _decorated(request, *args, **kwargs):
        admin_set = get_object_or_404(AdminSet, pk=1)
        try:
            invocador = request.user.invocador
        except Invocador.DoesNotExist:
            invocador = None
            return redirect("register-summoner")
        

        context_dict = {'user': request.user,
                        'icon': invocador.profile_icon,    
                        'api_key': admin_set.riot_api_key,
                        'key_valid': admin_set.status_key,
                        'current_patch': admin_set.current_patch,
                        'main_class': 'main'}
        
        if settings.DEBUG == True:
            return func(request, context_dict, *args, **kwargs)
        else:
            try:
                return func(request, context_dict, *args, **kwargs)
            except Http404:
                return render(request, '404.html')
            except Exception as e:
                return render(request, '404.html')


    return _decorated 