import datetime


def datetime_to_unix(dt):
    """
    Converte um objeto datetime para timestamp UNIX no padrão da API da Riot.
    """
    if dt is None:
        return None
    return int(dt.timestamp())