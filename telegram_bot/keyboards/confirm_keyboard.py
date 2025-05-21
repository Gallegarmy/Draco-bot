from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def build_confirm_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Cancelar", callback_data=f"cancel"),
            InlineKeyboardButton("Confirmar", callback_data=f"submit"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)