import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.commands.start import start
from bot.registratin import registration
from bot.keyboards.inline_keyboards.callbacks import callbacks
from bot.keyboards.reply_keyboards.reply_keyboard_process import reply
from bot.review import review
from bot.webhooks import webhooks
from bot.update import update
from aiohttp import web
from contextlib import suppress

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
APP_PORT = int(os.getenv('APP_PORT'))

bot = Bot(token=TELEGRAM_TOKEN)
Dp = Dispatcher()
Dp.include_routers(start,
                   registration,
                   update,
                   review,
                   callbacks,
                   reply,)


async def run_other_task(_app):
    task = asyncio.create_task(Dp.start_polling(bot))
    yield
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task


app = web.Application()
app.add_routes(webhooks)
app.cleanup_ctx.append(run_other_task)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, port=APP_PORT)
    print('Stop Server')