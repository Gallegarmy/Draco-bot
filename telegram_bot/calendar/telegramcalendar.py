#!/usr/bin/env python3
#
# A library that allows to create an inline calendar keyboard.
# grcanosa https://github.com/grcanosa
#
"""
Base methods for calendar keyboard creation and processing.
"""


from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove
import datetime
import calendar
from .messages import CALENDAR_CALLBACK
from utils.telegram_calendar_utils import separate_callback_data


def create_callback_data(action,year,month,day=None):
    """ Create the callback data associated to each button"""
    tokens = [str(action), str(year), str(month)]
    if day is not None:
        tokens.append(str(day))

    return CALENDAR_CALLBACK + ";" + ";".join(tokens)


def create_previous_month_info(action,year,month):
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    return create_callback_data(action, year, month)

    
def create_next_month_info(action,year,month):
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    return create_callback_data(action, year, month)


def create_calendar(time_event_description:str, year=None, month=None):
    """
    Create an inline keyboard with the provided year and month
    :param time_event_description: the title for the event to be created
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = datetime.datetime.now()
    if year == None: 
        year = now.year
    else:
        year = datetime.datetime.strptime(year, "%Y").year
    if month == None: 
        month = now.month
    else:
        month =  datetime.datetime.strptime(month, "%m").month
    display_only_button_data = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    #First row - Month and Year
    row=[]
    row.append(InlineKeyboardButton(calendar.month_name[month]+" "+str(year),callback_data=display_only_button_data))
    keyboard.append(row)
    #Second row - Week Days
    row=[]
    for day in ["Mo","Tu","We","Th","Fr","Sa","Su"]:
        row.append(InlineKeyboardButton(day,callback_data=display_only_button_data))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ",callback_data=display_only_button_data))
            else:
                if datetime.date(year, month, day) >= datetime.date.today():
                    row.append(InlineKeyboardButton(str(day), callback_data=create_callback_data(time_event_description, year, month, day)))
                else:
                    row.append(InlineKeyboardButton(" ", callback_data=display_only_button_data))
        keyboard.append(row)
    #Last row - Buttons
    row=[]
    row.append(InlineKeyboardButton("<",callback_data=create_previous_month_info("PREV-MONTH", year, month)))
    row.append(InlineKeyboardButton(" ",callback_data=display_only_button_data))
    row.append(InlineKeyboardButton(">",callback_data=create_next_month_info("NEXT-MONTH", year, month)))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


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
            reply_markup=create_calendar(int(pre.year),int(pre.month)))
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        context.bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(ne.year),int(ne.month)))
    else:
        context.bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")
        # UNKNOWN
    return ret_data
