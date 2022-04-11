from lk_utils import loads

from .paths import user_config as path

__all__ = ['user_config']


class T:
    from typing import TypedDict
    
    class UserConfig(TypedDict):
        predefined_paths: list[str]


try:
    user_config: T.UserConfig = loads(path)
except FileNotFoundError:
    raise Exception(
        'user config file not found: {}\n'
        'please copy "~/model/backup/user_config.yml" to '
        '"~/model/user_config.yml"'.format(path)
    )
