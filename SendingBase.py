import logging
import asyncio
import time
import lpr_const as lpr

from aiogram import Bot, Dispatcher, executor, types

from sqlighterBased import SQLighter

logging.basicConfig(level=logging.INFO)

    # инициализируем бота
bot = Bot(token='1533852346:AAEYXd6JymBNYJZDi52ISU1mh8TLhvMiQto')
dp = Dispatcher(bot)

    # инициализируем соединение с БД
db = SQLighter(lpr.dbase)

@dp.message_handler(commands=['sendingBaseReg']) #Команда, которая осуществляет массовую рассылку по собранной базе пользователей. Команду может использовать только человек, указанный в хендлере (user_id)
async def welcome(message: types.Message):
    if message.from_user.id == lpr.host_admin or message.from_user.id == lpr.reg_admin:
        db.send_base_reg()
        db.send_base_mos()
        doc1 = open ("result_reg.xlsx", "rb")
        doc2 = open("result_mos.xlsx", "rb")
        await bot.send_document(message.chat.id, doc1)
        doc1.close()
        await bot.send_document(message.chat.id, doc2)
        doc2.close()

@dp.message_handler(commands=['sendingBaseMos']) #Команда, которая осуществляет массовую рассылку по собранной базе пользователей. Команду может использовать только человек, указанный в хендлере (user_id)
async def welcome(message: types.Message):
      if message.from_user.id == lpr.host_admin or message.from_user.id == lpr.mos_admin:
        db.send_base_mos()
        doc2 = open("result_mos.xlsx", "rb")
        await bot.send_document(message.chat.id, doc2)
        doc2.close()


@dp.message_handler(commands=['SendingCheck'])
async def check (message: types.Message):
    if message.from_user.id == lpr.host_admin or message.from_user.id == lpr.mos_admin:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_one = types.KeyboardButton('Идентификация по юзернейму')
        item_two = types.KeyboardButton('Идентификация по user_id')

        markup.add(item_one, item_two)

        await message.answer('Каким способом вы хотите идентифицировать пользователя?', reply_markup=markup)

    else:
        pass
@dp.message_handler(text=['Идентификация по юзернейму'])
async def check_username(message: types.Message):
    if message.from_user.id == lpr.host_admin or message.from_user.id == lpr.mos_admin:
        await message.answer ('Введите юзернейм')
        print (message.text)
    else:
        pass







@dp.message_handler(text=['Идентификация по user_id'])
async def check_user_id(message: types.Message):
    if message.from_user.id == lpr.host_admin or message.from_user.id == lpr.mos_admin:
        await message.answer ('Введите user_id')
        print (message.text)
    else:
        pass

@dp.message_handler(content_types=['text'])
async def modify_message(message: types.Message):
    if message.from_user.id == lpr.host_admin or message.from_user.id == lpr.mos_admin:
        if db.subscriber_exists(message.text):
            await message.answer ('Пользователь участвовал в переучете')

        else:
            username_mes = message.text.replace("@", "")
            print (username_mes)
            if db.subscriber_exists_username_reg(username_mes) or db.subscriber_exists_username_msk(username_mes):
                await message.answer('Пользователь участвовал в переучете')


            else:

                await message.answer ('Пользователь не найден в базе')
    else:
        pass
if __name__ == '__main__':
  executor.start_polling(dp)