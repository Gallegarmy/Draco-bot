from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def build_meeting_type_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🔓 Abierta", callback_data="Abierta"),
            InlineKeyboardButton("🔒 Cerrada", callback_data="Cerrada")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)