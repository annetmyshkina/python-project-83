from validators import url
from urllib.parse import urlparse


def normalize_url(url_name):
    if not url_name:
        return False, "URL обязателен"

    if len(url_name) > 255 and url(url_name):
        return False, "Некорректный URL"

    parsed = urlparse(url_name)
    if not (parsed.scheme and parsed.netloc):
        return False, "Некорректный URL"

    domain = f"{parsed.scheme}://{parsed.netloc}"
    return True, domain