from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def build_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("✅ Unirse", callback_data="join"),
            InlineKeyboardButton("➕ +1", callback_data="+1")
        ],
        [
            InlineKeyboardButton("❌ Dejar", callback_data="leave"),
            InlineKeyboardButton("➖ -1", callback_data="-1")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)