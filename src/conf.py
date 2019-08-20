import os

def get_conf(key, default=None, t=str):
    mockconf = {
        'HOST': '127.0.0.1',
        'PORT': 3853,
        'DNS_HOST': '8.8.8.8',
        'DNS_PORT': 853,
    }
    value = mockconf.get(key.upper(), default)
    if t is not str:
        return t(value)

    return value
    # return os.getenv(key.upper(), default)
