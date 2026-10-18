from dataclasses import dataclass

from environs import Env


@dataclass
class Bot:
    token: str

@dataclass
class Logging:
    format: str
    level: str
    file: str

@dataclass
class DataBase:
    password: str
    host: str
    port: int

@dataclass
class API:
    url: str

@dataclass
class Config:
    bot: Bot
    log: Logging
    db: DataBase
    api: API

def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)

    return Config(
        bot=Bot(
            token=env("BOT_TOKEN"),
        ),
        log=Logging(
            format=env("LOG_FORMAT"),
            level=env("LOG_LEVEL"),
            file=env("LOG_FILE"),
        ),
        db=DataBase(
            password=env("DB_PASSWORD"),
            host=env("DB_HOST"),
            port=env.int("DB_PORT", default=6379),
        ),
        api=API(
            url='https://cataas.com/cat?json=true',
        ),
    )