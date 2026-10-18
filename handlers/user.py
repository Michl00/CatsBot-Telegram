import aiohttp
from aiogram import Bot, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis.asyncio import Redis

from config.config import Config
from lexicon.lexicon import LEXICON_RU
from services.services import send_cat

user_router = Router()

@user_router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(LEXICON_RU['help'])


@user_router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(LEXICON_RU['help'])


@user_router.message(Command("cat"))
async def cat_handler(message: Message, session: aiohttp.ClientSession, config: Config, bot: Bot):
    await send_cat(session=session, chat_id=message.chat.id, config=config, bot=bot)


@user_router.message(Command("time"))
async def choose_time(message: Message, db: Redis):
    chat_id = message.chat.id
    user_key = f'user:{chat_id}'

    user_exists = await db.exists(user_key)

    if not user_exists:
        await db.hset(user_key, mapping={
            'is_subscribed': '0',
            'interval': '0',
            'last_send': '0',
        })

    await db.sadd('bot:users', chat_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 час", callback_data="set_time:1")],
        [InlineKeyboardButton(text="2 часа", callback_data="set_time:2")],
        [InlineKeyboardButton(text="другое время", callback_data="set_time:custom")],
    ])
    await message.answer(LEXICON_RU['choose_interval'], reply_markup=keyboard)


@user_router.message(Command("stop"))
async def unsubscribe(message: Message, db: Redis, scheduler: AsyncIOScheduler):
    chat_id = message.chat.id
    user_key = f'user:{chat_id}'

    user_exists = await db.exists(user_key)

    if user_exists:
        await db.hset(user_key, "is_subscribed", "0")

        try:
            scheduler.remove_job(str(chat_id))
        except JobLookupError:
            pass

        await message.answer(LEXICON_RU['unsubscribe'])
    else:
        await message.answer(LEXICON_RU['error:not_subscribed'])
