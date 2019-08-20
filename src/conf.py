import os

def get_conf(key, default=None, t=str):
    mockconf = {
        'HOST': '127.0.0.1',
        'PORT': 3853,
        'DNS_HOST': '8.8.8.8',
        'DNS_PORT': 853,
    }
    # value = mockconf.get(key.upper(), default)

    # We can't use the second parameter to `getenv` because we don't want to
    # cast the default value, we just want to return it as-is.
    value = os.getenv(key)
    if value:
        if t is str:
            return value
        else:
            return t(value)

    return default
