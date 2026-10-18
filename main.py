import asyncio
import logging

import aiohttp
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis.asyncio import Redis

from config.config import Config, load_config
from handlers.other import other_router
from handlers.user import user_router
from services.services import restore_schedule

config : Config = load_config()

bot = Bot(config.bot.token)
dp = Dispatcher()

logging.basicConfig(
    format=config.log.format,
    level=config.log.level,
    filename=config.log.file,
    filemode='w',
)
logger = logging.getLogger(__name__)

db = Redis(
    host=config.db.host,
    port=config.db.port,
    password=config.db.password,
    db=0,
    decode_responses=True,
)

scheduler = AsyncIOScheduler()

async def main():
    logger.info('Starting bot.')

    dp.include_router(user_router)
    dp.include_router(other_router)

    async with aiohttp.ClientSession() as session:
        dp['session'] = session
        dp['config'] = config
        dp['db'] = db
        dp['scheduler'] = scheduler

        await restore_schedule(session, db, scheduler, bot, config)

        scheduler.start()

        try:
            await dp.start_polling(bot)
        finally:
            scheduler.shutdown()
            await db.aclose()
            await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")