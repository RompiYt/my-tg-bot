import asyncio
from xmlrpc import client
from aiogram import Bot, F
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from config import TOKEN
from dispatcher import dp, router
from logging_setup import setup_logging
import logging
from aiogram.enums import ParseMode
import sys
from dispatcher import dp
from openai import AsyncClient

AI_TOKEN = "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"

async def generate_response(prompt):
    client = AsyncClient(
        base_url="https://openrouter.ai/api/v1",
        api_key=AI_TOKEN,
    )

    system_message = (
        "Ты — виртуальный психолог‑консультант. Твоя задача: "
        "поддерживать, выслушивать и давать мягкие, безопасные советы "
        "по повседневным вопросам (отношения, работа, учёба, хобби, планирование, стресс). "
        
        "Правила работы: "
        "- Не углубляйся в прошлое, не проводи психоанализ. "
        "- Фокусируйся на практических шагах: как успокоиться, спланировать день, "
          "выразить чувства, наладить коммуникацию. "
        "- Используй поддерживающий, тёплый тон без осуждения. "
        "- Если информации мало, задай 1–2 мягких уточняющих вопроса. "
        "- Ответы — короткими абзацами, без жаргона, максимально понятно."
    )

    completion = await client.chat.completions.create(
        extra_body={},
        model="qwen/qwq-32b",
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )   
    return completion.choices[0].message.content


@dp.message()
async def echo_handler(message: Message) -> None:
    msg = await message.answer("Готовлю ответ..")
    response = await generate_response(message.text)
    await msg.delete()
    await message.answer(f'{response}')

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

