import calendar
import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram_bot.calendar.messages import CALENDAR_CALLBACK


def create_calendar_keyboard(time_event_description:str, year=None, month=None):
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


def create_callback_data(action,year,month,day=None):
    """
    Create the callback data associated to each button with structure:
        eg. CALENDAR;PREV-MONTH;2025;6
        eg. CALENDAR;NEXT-MONTH;2025;5;25
    """
    tokens = [str(action), str(year), str(month)]
    if day is not None:
        tokens.append(str(day))

    return CALENDAR_CALLBACK + ";" + ";".join(tokens)