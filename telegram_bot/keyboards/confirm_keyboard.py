from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def build_confirm_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Confirmar", callback_data=f"submit"),
            InlineKeyboardButton("Cancelar", callback_data=f"cancel"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)