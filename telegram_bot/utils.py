import structlog
from telegram import Update

logger = structlog.get_logger()

async def get_username(update: Update):
    logger.info(
        "get_username() function called",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )
    user = None
    if update.message and update.message.from_user:
        user = update.message.from_user
    elif update.callback_query and update.callback_query.from_user:
        user = update.callback_query.from_user

    if user is None:
        if update.effective_message and update.effective_message.from_user:
            user = update.effective_message.from_user

    if user is None:
        if update.effective_chat:
            await update.effective_chat.send_message(
                text="Necesítase un username ou nome en Telegram para interactuar co bot.",
                message_thread_id=await get_thread_id(update),
            )
        return None

    if user.username:
        request_user = user.username
    elif user.first_name:
        request_user = user.first_name
    elif user.full_name:
        request_user = user.full_name
    else:
        if update.effective_chat:
            await update.effective_chat.send_message(
                text="Necesítase un username ou nome en Telegram para interactuar co bot.",
                message_thread_id=await get_thread_id(update),
            )
        return None
    return request_user


async def get_thread_id(update: Update):
    if update.effective_message:
        thread_id = update.effective_message.message_thread_id
        return thread_id
    return None

def is_fullgame(context, event_id):
    current_players = len(context.chat_data[event_id]["players"].keys())
    current_guests = sum(context.chat_data[event_id]["players"].values())
    total_players = current_players + current_guests
    is_full_game = total_players >= int(context.chat_data[event_id]["max_players"])
    return is_full_game