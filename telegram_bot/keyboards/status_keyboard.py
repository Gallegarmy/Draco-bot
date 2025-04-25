from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def build_status_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🔓 Abierta", callback_data="Open"),
            InlineKeyboardButton("🔒 Cerrada", callback_data="Closed")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)