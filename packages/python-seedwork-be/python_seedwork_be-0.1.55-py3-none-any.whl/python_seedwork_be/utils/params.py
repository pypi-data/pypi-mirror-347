import os

from dotenv import load_dotenv
from returns.curry import partial


def cast_bool_from_str(value):
    if value.lower() in ["true", "yes", "on", "1"]:
        value = True
    elif value.lower() in ["false", "no", "not", "off", "0"]:
        value = False
    else:
        raise ValueError(
            f'Incorrect value: "{value}". '
            f"It should be one of [1, 0, true, false, yes, no]"
        )
    return value


def get_env(name, default=None, is_bool=False, env="local"):
    load_dotenv(f".{env}.env")
    value = os.environ.get(name)
    if value is not None:
        if is_bool:
            return cast_bool_from_str(value)
        else:
            return value
    return default


def get_environment() -> str:
    return os.environ.get("ENV", default="local")


def get_env_with(env: str):
    return partial(get_env, env=env)
