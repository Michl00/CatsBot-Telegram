import logging
import time

import aiohttp
from aiogram import Bot
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis.asyncio import Redis

from config.config import Config
from lexicon.lexicon import LEXICON_RU

logger = logging.getLogger(__name__)


async def add_user(
        chat_id: int,
        interval: int,
        session: aiohttp.ClientSession,
        message: Message,
        db: Redis,
        scheduler: AsyncIOScheduler,
        bot: Bot,
        config: Config
    ):
    user_key = f"user:{chat_id}"

    await db.hset(user_key, mapping={
        "is_subscribed": "1",
        "interval": str(interval),
        "last_send": str(time.time())
    })

    await db.sadd("bot:users", chat_id)

    scheduler.add_job(
        cat_sender,
        trigger="interval",
        hours=interval,
        args=[session, chat_id, bot, db, config],
        id=str(chat_id),
        replace_existing=True
    )

    await message.answer(LEXICON_RU['set_interval'] % interval)


async def send_cat(
        session: aiohttp.ClientSession,
        chat_id: int,
        config: Config,
        bot: Bot
    ):
    try:
        async with session.get(config.api.url) as response:
            if response.status == 200:
                data = await response.json()
                photo_url = data.get('url')
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=photo_url,
                    caption=LEXICON_RU['your_cat'],
                )
            else:
                await bot.send_message(
                    chat_id=chat_id,
                    text=LEXICON_RU['error:cat_send'],
                )
    except Exception:
        logger.exception("Failed to send initial cat to %s", chat_id)


async def cat_sender(
        session: aiohttp.ClientSession,
        chat_id: int,
        bot: Bot,
        db: Redis,
        config: Config
    ):
    user_key=f'user:{chat_id}'

    try:
        await send_cat(session, chat_id, config, bot)
        await db.hset(user_key, 'last_send', str(time.time()))

    except Exception:
        logger.exception("Failed to send cat to %s", chat_id)


async def restore_schedule(
        session: aiohttp.ClientSession,
        db: Redis,
        scheduler: AsyncIOScheduler,
        bot: Bot,
        config: Config
    ):
    user_ids = await db.smembers("bot:users")
    for user_id in user_ids:
        user_key = f"user:{user_id}"
        user_data = await db.hgetall(user_key)

        if user_data.get("is_subscribed") == "1":
            interval = int(user_data.get("interval", 1))

            scheduler.add_job(
                cat_sender,
                trigger="interval",
                hours=interval,
                args=[session, int(user_id), bot, db, config],
                id=str(user_id),
                replace_existing=True
            )
    logger.info("All jobs are succesfully restored from Redis.")