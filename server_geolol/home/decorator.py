from django.shortcuts import render, redirect, get_object_or_404
from riot_admin.models import *

def profile_user_data(func):
    def _decorated(request, *args, **kwargs):
        admin_set = get_object_or_404(AdminSet, pk=1)        
        context_dict = {'user': request.user,
                        'icon': request.user.invocador.profile_icon,
                        'api_key': admin_set.riot_api_key}
        return func(request, context_dict, *args, **kwargs)
    return _decorated 