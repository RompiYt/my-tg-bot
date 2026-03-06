from aiogram import Dispatcher
from tgbott.handlers import router

dp = Dispatcher()
dp.include_router(router)  
