import logging
import uvicorn
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types

from src import load_config
from src.tgbot.handlers.start import register_start

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)


def register_all_handlers(dp: Dispatcher):
    register_start(dp)


config = load_config(".env")
storage = MemoryStorage()

WEBHOOK_PATH = f"/bot/{config.tg.token}"
WEBHOOK_URL = config.tg.webhook_url + WEBHOOK_PATH

app = FastAPI()
bot = Bot(token=config.tg.token, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)


@app.on_event("startup")
async def on_startup():
    logger.info("Bot started")
    webhook_info = await bot.get_webhook_info()
    if webhook_info != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )
    register_all_handlers(dp)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
