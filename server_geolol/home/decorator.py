def profile_user_data(func):
    def _decorated(request, *args, **kwargs):        
        context_dict = {'user': request.user,
                        'icon': request.user.invocador.profile_icon}
        return func(request, context_dict, *args, **kwargs)
    return _decorated 