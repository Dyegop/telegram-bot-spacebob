""" Manage bot functionalities """

import logging
import src.functionalities.forecast as forecast
from telegram import Update, ParseMode, error
from telegram.ext import CallbackContext, ConversationHandler


# LOG
logger = logging.getLogger(__name__)


USER_DATA = {
    "LOCATION": {
        "lat": "0",
        "lon": "0",
    }
}


def start(update: Update, context: CallbackContext):
    """
    Start the bot
    :param update: telegram.Update object
    :param context: telegram.ext.CallbackContext object

    context.bot.send_message()  -> send message to the user
    update.message.reply_text() -> shortcut for context.bot.send_message()
    update.effective_chat.id    -> return current chat_id
    """
    welcome = "Welcome human! \U0001F916 \U0001F411"
    # context.bot.send_message(chat_id=update.effective_chat.id, text=welcome)
    update.message.reply_text(welcome)


def stop(update: Update, context: CallbackContext):
    """
    Stop scheduled job
    :param update: telegram.Update object
    :param context: telegram.ext.CallbackContext object

    Usage: /stop command1 command2
    Commands that starts jobs and those given jobs must have the same name

    context.job_queue.get_jobs_by_name("job_name") -> get job object by name
    schedule_removal()                             -> remove scheduled job
    """
    for i in context.args:
        job = context.job_queue.get_jobs_by_name(i)
        job[0].schedule_removal()
        update.message.reply_text(f'<b>Command {i} stopped</b>', parse_mode=ParseMode.HTML)


def botver(update: Update, context: CallbackContext):
    """ Return bot version """
    update.message.reply_text("v22-02-2022.01-AlphaRelease")


def cancel(update: Update, context: CallbackContext):
    """ Cancel any command in a ConversationHandler"""
    update.message.reply_text('Command canceled')
    return ConversationHandler.END


def send_location(update: Update, context: CallbackContext) -> int:
    """ Return initial state for location_handler in bot.Handlers() class """
    update.message.reply_text('Share your current location \U0001F4CD\n'
                              'Send /cancel to exit')
    return 0


def get_map_coordinates(update: Update, context: CallbackContext):
    """ Update user current location """
    USER_DATA["LOCATION"]["lat"], USER_DATA["LOCATION"]["lon"] = (update.message.location.latitude,
                                                                  update.message.location.longitude)
    update.message.reply_text('Location has been updated')
    return ConversationHandler.END


def get_forecast(context, welcome):
    """ Return current weather for stored location """
    try:
        forecast_obj = forecast.Forecast(USER_DATA["LOCATION"]["lat"],
                                         USER_DATA["LOCATION"]["lon"])
        w, temp, loc = forecast_obj.request_forecast_data()
        # Send message with results
        context.bot.send_message(chat_id=context.job.context, text=(
            f'{welcome}\n'
            f'{forecast_obj.get_city_from_coordinates()}: {temp["temp"]:.1f}ºC '
            f'(feels like: {temp["feels_like"]:.1f}ºC)\n'
            f'Max: {temp["temp_max"]:.1f}ºC - Min: {temp["temp_min"]:.1f}ºC\n'
            f'{w["main"]} - {w["description"]} {forecast_obj.weather_emoji(w["id"]) * 2}'))
    except error.BadRequest:
        logging.error("Chat_id is empty")





'''def forecast(update: Update, context: CallbackContext):
    """
    Set forecast notification over time

    context.job_queue -> jobQueue asociated with this context
    """
    update.message.reply_text("Forecast notifications activated"
                              'A message will be delivered from 09:00 AM every 6 hours')
    # Run every 6h from 09:00:00 AM
    context.job_queue.run_repeating(getForecast, interval=21600, first=datetime.time(9, 0, 0, 0),
                                    context=update.message.chat_id, name="forecast")'''
