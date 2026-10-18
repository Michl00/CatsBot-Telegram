import aiohttp
from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from redis.asyncio import Redis

from config.config import Config
from lexicon.lexicon import LEXICON_RU
from services.services import add_user, send_cat

other_router = Router()

class Form(StatesGroup):
    waiting_for_hours = State()

@other_router.callback_query(F.data.startswith('set_time:'))
async def time_selection(
    callback: CallbackQuery,
    session: aiohttp.ClientSession,
    db: Redis,
    bot: Bot,
    scheduler: AsyncIOScheduler,
    config: Config,
    state: FSMContext
):
    if not callback.data or not isinstance(callback.message, Message):
        return

    try:
        scheduler.remove_job(str(callback.message.chat.id))
    except JobLookupError:
        pass

    selected_value = callback.data.split(':')[1]
    chat_id = callback.message.chat.id

    if selected_value == "custom":
        await callback.message.edit_text(LEXICON_RU['enter_hours'])
        await state.set_state(Form.waiting_for_hours)
        return

    interval = int(selected_value)

    await add_user(
        chat_id=chat_id,
        interval=interval,
        session=session,
        message=callback.message,
        db=db,
        scheduler=scheduler,
        bot=bot,
        config=config
    )

    await send_cat(session=session, chat_id=chat_id, config=config, bot=bot)

    await callback.answer()


@other_router.message(Form.waiting_for_hours)
async def handle_custom_hours(message: Message,
                              state: FSMContext,
                              session: aiohttp.ClientSession,
                              db: Redis,
                              bot: Bot,
                              scheduler: AsyncIOScheduler,
                              config: Config,
                              ):
    if not message.text:
        await message.answer(LEXICON_RU['error:hours'])
        return

    try:
        hours = int(message.text)
    except ValueError:
        await message.answer(LEXICON_RU['error:hours'])
        return

    if hours <= 0:
        await message.answer(LEXICON_RU['error:hours_negative'])
        return

    await add_user(chat_id=message.chat.id,
                   interval=hours,
                   session=session,
                   db=db,
                   scheduler=scheduler,
                   bot=bot,
                   config=config,
                   message=message
                   )
    await state.clear()