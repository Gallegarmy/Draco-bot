from telegram import InlineKeyboardButton

def build_status_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🔓 Abierta", callback_data="abierta"),
            InlineKeyboardButton("🔒 Cerrada", callback_data="cerrada")
        ]
    ]
    return keyboard