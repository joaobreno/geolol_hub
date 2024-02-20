def profile_user_data(func):
    def _decorated(request, *args, **kwargs):
        user_settings = {'username': request.user.username,
                         'summoner_name': request.user.invocador.nome_invocador,
                         'summoner_tag': request.user.invocador.tag}
        
        context_dict = {'user': user_settings}
        return func(request, context_dict, *args, **kwargs)
    return _decorated 