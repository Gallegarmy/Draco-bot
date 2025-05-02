from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime


def build_time_keyboard(time_event_description: str):
    keyboard = []
    

    # Generate list of hour strings 
    remaining_hours = list(range(24))
    for hour in remaining_hours:
        option=[InlineKeyboardButton(f"{hour}:00", callback_data=f"{time_event_description}-{hour}:00"),
                InlineKeyboardButton(f"{hour}:30", callback_data=f"{time_event_description}-{hour}:30")]
        keyboard.append(option)
    return InlineKeyboardMarkup(keyboard)