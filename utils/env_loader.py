from config.settings import SETTINGS


def get_env_value(key: str, default=None):
    return SETTINGS.get(key, default)
