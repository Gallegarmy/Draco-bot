from telegram import Update,  InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.logger import logger
from shared import joined
from .message_builder import build_message
from .keyboard_builder import build_keyboard

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    user_id = user.id
    action = query.data

    # Ensure the user is in the dict
    if user_id not in joined:
        joined[user_id] = {"name": user.full_name, "guests": 0}

    if action == "join":
        joined[user_id]["guests"] = 0
        await query.answer("You joined!")
    elif action == "+1":
            joined[user_id]["guests"] += 1
            await query.answer("You joined with +1!")
    elif action == "leave":
        if user_id in joined:
            del joined[user_id]
        await query.answer("You left.")
    elif action == "-1":
        if user_id in joined and joined[user_id]["guests"] > 0:
            joined[user_id]["guests"] -= 1
            await query.answer("Removed one guest.")
        else:
            await query.answer("No guests to remove.", show_alert=True)
    message = build_message(joined)
    reply_markup = InlineKeyboardMarkup(build_keyboard())
    await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')