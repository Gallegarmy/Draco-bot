from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def build_attendance_keyboard(event_id):
    keyboard = [
        [
            InlineKeyboardButton("✅ Unirse", callback_data=f"{event_id},join"),
            InlineKeyboardButton("➕ +1", callback_data=f"{event_id},+1")
        ],
        [
            InlineKeyboardButton("❌ Dejar", callback_data=f"{event_id},leave"),
            InlineKeyboardButton("➖ -1", callback_data=f"{event_id},-1")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


