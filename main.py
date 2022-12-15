from contextlib import suppress

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, ChatJoinRequest, ChatType
from dotenv import dotenv_values

config = dotenv_values('.env')

bot = Bot(config.get('BOT_TOKEN'))
dp = Dispatcher(bot)

start_text = '''Hey, I am Bot!

I remove messages about user joined or left chatroom.
Accept a request to subscribe to a private telegram channel
'''


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    await message.reply(start_text)


@dp.message_handler(content_types=('new_chat_members', 'left_chat_member'))
async def echo(message: Message):
    if message.new_chat_members[0].id == bot.id:
        await message.answer(start_text)
    else:
        with suppress(Exception):
            await message.delete()


@dp.chat_join_request_handler(lambda x: ChatType.CHANNEL)
async def join(update: ChatJoinRequest):
    await update.approve()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
