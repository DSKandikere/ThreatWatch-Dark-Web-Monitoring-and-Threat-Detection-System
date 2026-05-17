import requests
from config.settings import TOR_PROXY

def get_tor_session():
    session = requests.session()
    session.proxies = {
        'http': TOR_PROXY,
        'https': TOR_PROXY
    }
    return session
