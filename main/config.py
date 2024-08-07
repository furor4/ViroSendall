from aiogram import Bot, Dispatcher
from environs import Env
from aiogram.fsm.storage.memory import MemoryStorage

env = Env()
env.read_env('info.env')

TOKEN = env.str('TOKEN')
ADMIN1 = env.int('ADMIN_V')
ADMIN2 = env.int('ADMIN_C')
ADMIN3 = env.int('ADMIN_N')
CHAT_ID = env.str('CHAT_ID')
bot = Bot(token=TOKEN)

dp = Dispatcher(storage=MemoryStorage())
