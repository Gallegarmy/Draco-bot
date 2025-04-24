from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime


def build_time_keyboard(time_event_description: str):
    keyboard = []
    # Get the current hour and add 1 to start from the next hour
    current_hour = datetime.now().hour + 1

    # Generate list of hour strings from the next hour up to 23
    remaining_hours = [str(hour) for hour in range(current_hour, 24)]
    for hour in remaining_hours:
        option=[InlineKeyboardButton(f"{hour}:00", callback_data=f"{time_event_description}-{hour}:00"),
                InlineKeyboardButton(f"{hour}:30", callback_data=f"{time_event_description}-{hour}:30")]
        keyboard.append(option)
    return InlineKeyboardMarkup(keyboard)