from telegram import InlineKeyboardMarkup, InlineKeyboardButton

TOP_LIMIT_PLAYERS = 30

BUTTONS_PER_ROW = 5

def create_num_keyboard() -> InlineKeyboardMarkup:
    result = []
    row = []
    for num in ("2", "3", "4", "5"):
        row.append(InlineKeyboardButton(num, callback_data=num))
    result.append(row)

    first_row_button_index = BUTTONS_PER_ROW
    while first_row_button_index < TOP_LIMIT_PLAYERS:
        row = []
        for column in range(1,6):
            row.append(InlineKeyboardButton(str(first_row_button_index + column), callback_data=str(first_row_button_index + column)))
        first_row_button_index += BUTTONS_PER_ROW
        result.append(row)


    return InlineKeyboardMarkup(result)