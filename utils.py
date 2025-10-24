import validators

def validar_url(url: str) -> bool:
    return validators.url(url)