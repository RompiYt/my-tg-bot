
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
import logging
from config import CURATOR_ID
from database import add_to_database
from keyboards import main_keyboard, cancel_keyboard, get_reply_keyboard
from openai import AsyncClient

AI_TOKEN = "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"

router = Router()
user_states = {}

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Привет! Это бот, который анонимно будет помогать тебе с твоей проблемой и предложит решения. "
        "Так же ты можешь связаться с нашими психологами и обсудить это более подробно. "
        "С какой проблемой ты столкнулся? Опиши её.",
        reply_markup=main_keyboard
    )
    telegram_id = message.from_user.id
    username = message.from_user.username
    await add_to_database(telegram_id, username)
    user_states[telegram_id] = None

@router.message()
async def handle_message(message: Message) -> None:
    user_id = message.from_user.id
    text = message.text

    if user_states.get(user_id) and "reply_to" in user_states[user_id]:
        target_user_id = user_states[user_id]["reply_to"]
        try:
            await message.bot.send_message(
                chat_id=target_user_id,
                text=f"Ответ куратора:\n\n{text}"
            )
            await message.answer("Ответ отправлен пользователю.")
            logging.info(f"Куратор {user_id} ответил пользователю {target_user_id}")
        except Exception as e:
            logging.error(f"Ошибка отправки ответа пользователю: {e}")
            await message.answer("Не удалось отправить ответ. Попробуйте позже.")
        user_states[user_id] = None
        return

    if text == "Обратиться к специалисту":
        user_states[user_id] = "waiting_for_problem"
        await message.answer("Опишите проблему:", reply_markup=cancel_keyboard)
    
    elif text == "Отменить":
        if user_states.get(user_id) == "waiting_for_problem":
            user_states[user_id] = None
            await message.answer("Действие отменено. Вы можете продолжить общение с ботом.", reply_markup=main_keyboard)
        else:
            await message.answer("Нет активного действия для отмены.", reply_markup=main_keyboard)
    
    elif user_states.get(user_id) == "waiting_for_problem":
        try:
            bot = message.bot  
            keyboard = get_reply_keyboard(user_id)  
            await bot.send_message(
                chat_id=CURATOR_ID,
                text=(
                    f"Новое сообщение от пользователя @{message.from_user.username} "
                    f"(ID: {user_id}):\n\n{text}"
                ),
                reply_markup=keyboard 
            )
            await message.answer("Ваше сообщение отправлено куратору. Ожидайте ответа.", reply_markup=main_keyboard)
            logging.info(f"Сообщение от {user_id} успешно отправлено куратору")
        except Exception as e:
            logging.error(f"Ошибка отправки сообщения куратору: {e}")
            await message.answer(
                "Не удалось отправить сообщение куратору. "
                "Пожалуйста, попробуйте позже или свяжитесь напрямую: @куратор_ник",
                reply_markup=main_keyboard
            )   
        user_states[user_id] = None

@router.callback_query(F.data.startswith("reply_"))
async def handle_reply_button(callback: CallbackQuery):
    await callback.answer() 
    user_id = int(callback.data.split("_")[1]) 
    curator_id = callback.from_user.id
    user_states[curator_id] = {"reply_to": user_id}
    await callback.message.answer(
        f"Вы готовы ответить пользователю {user_id}. Напишите ответ:"
    )

async def generate_response(prompt):
    client = AsyncClient(
        base_url="https://openrouter.ai/api/v1",
        api_key=AI_TOKEN,
    )

    completion = await client.chat.completions.create(
        extra_body={},
        model="qwen/qwq-32b",
        messages=[
            {
            "role": "user",
            "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content

@router.message()
async def echo_handler(message: Message) -> None:
    msg = await message.answer('Нейросеть готовит ответ')
    response = await generate_response(message.text)
    await msg.delete()

    await message.answer(f'{response}')
