#!/usr/bin/env python3
#
# A library that allows to create an inline calendar keyboard.
# grcanosa https://github.com/grcanosa
#
"""
Base methods for calendar keyboard creation and processing.
"""

import datetime
from utils.telegram_calendar_utils import separate_callback_data
from ..keyboards.calendar_keyboard import create_calendar_keyboard


def process_calendar_selection(update,context):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    :param telegram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param telegram.Update update: The update, as provided by the CallbackQueryHandler
    :return: Returns a tuple (Boolean,datetime.datetime), indicating if a date is selected
                and returning the date if so.
    """
    ret_data = (False,None)
    query = update.callback_query
    (_,action,year,month,day) = separate_callback_data(query.data)
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        context.bot.answer_callback_query(callback_query_id= query.id)
    elif action == "DAY":
        context.bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
            )
        ret_data = True,datetime.datetime(int(year),int(month),int(day))
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        context.bot.edit_message_text(text=query.message.text,
                                      chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      reply_markup=create_calendar_keyboard(int(pre.year), int(pre.month)))
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        context.bot.edit_message_text(text=query.message.text,
                                      chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      reply_markup=create_calendar_keyboard(int(ne.year), int(ne.month)))
    else:
        context.bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
        # UNKNOWN
    return ret_data
