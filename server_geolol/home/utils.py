import datetime


def datetime_to_unix(dt):
    """
    Converte um objeto datetime para timestamp UNIX no padrão da API da Riot.
    """
    if dt is None:
        return None
    return int(dt.timestamp())

def _log_console_title_section(title):
    section_title = f'X=================== {title} ===================X'
    print(section_title)
    return len(section_title)

def _log_console_item_section(qty):
    section = '-' * qty
    print(section)