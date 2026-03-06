from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Обратиться к специалисту")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отменить")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

def get_reply_keyboard(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Ответить пользователю",
            callback_data=f"reply_{user_id}"
        )]
    ])
    return keyboard

