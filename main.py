"""
PROJECT - TELEGRAM BOT

DOCUMENTATION
-https://python-telegram-bot.readthedocs.io/en/stable/index.html
-https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.callbackcontext.html
-https://python-telegram-bot.readthedocs.io/en/latest/telegram.update.html

NOTES
-Every bot command is an HTTP request, that requires an Update

-Telegram API only supports UTF-8, but Python works with Unicode
-Emojis in Unicode begins with U0000 or U0001
"""

import time
import logging
import src.base as base
import src.bot as bot
from pathlib import Path



# Log
def get_log():
    log_handler = logging.FileHandler(f'./logs/log_filename_{time.strftime("%Y%m%d")}.log', 'w', 'utf-8')
    log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(log_handler)




if __name__ == "__main__":
    get_log()

    # Setup settings
    params = base.Parameters()

    # Create bot and handlers
    telegram_bot = bot.SpaceBob(params.telegram_bot_token)
    handlers = bot.BotHandlers()

    # Add handlers
    telegram_bot.add_handlers(handlers.start_handler,
                              handlers.stop_handler,
                              handlers.botver_handler,
                              handlers.location_handler,
                              handlers.forecast_handler)


    # Start the Bot
    telegram_bot.start()
