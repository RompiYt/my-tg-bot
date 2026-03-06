from aiogram import Dispatcher
from handlers import router

dp = Dispatcher()
dp.include_router(router)  

