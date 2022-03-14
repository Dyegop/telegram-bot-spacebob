import logging
import src.commands as commands
from telegram.ext import Updater, Handler, CommandHandler, ConversationHandler, MessageHandler, Filters


# LOG
logger = logging.getLogger(__name__)



class SpaceBob:
    def __init__(self, bot_token: str):
        self._updater = Updater(bot_token)
        self._dispatcher = self._updater.dispatcher

    def add_handlers(self, *args: Handler) -> None:
        """ Add handlers to the dispatcher """
        for handler in args:
            self._dispatcher.add_handler(handler)
            logger.debug(f"Added handler {handler}")

    def start(self):
        """ Start the bot """
        # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
        # This should be used most of the time, since start_polling() is non-blocking and will stop the bot gracefully
        self._updater.start_polling()
        self._updater.idle()



class BotHandlers:
    """
    Manage bot handlers
    For more information about ConversationHandler implementation, see link below:
    https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.conversationhandler.html
    """

    start_handler = CommandHandler('start', commands.start)
    stop_handler = CommandHandler('stop', commands.stop, pass_args=True)
    botver_handler = CommandHandler('botver', commands.botver)
    location_handler = ConversationHandler(
        entry_points=[CommandHandler('send_location', commands.send_location, Filters.text)],
        states={0: [MessageHandler(Filters.location, commands.get_map_coordinates)]},
        fallbacks=[CommandHandler('cancel', commands.cancel)])
    forecast_handler = CommandHandler('forecast', commands.get_forecast)
