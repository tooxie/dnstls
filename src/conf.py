import os

def get_conf(key, default=None, t=str):
    """Gets a config value from an environment variable. If a `default` is not
    provided (or is None) and the key is not found in the environment, an
    exception will be raised. This is used to prevent misconfigurations from
    silently failing in production.
    """
    # We can't use the second parameter to `getenv` because we don't want to
    # cast the default value, we just want to return it as-is.
    value = os.getenv(key)
    if value:
        if t is str:
            return value
        else:
            return t(value)
    else:
        if default is None:
            raise ValueError(f'Config {key} not found')

    return default
