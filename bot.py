from aiogram import types, executor, Bot, Dispatcher
from aiogram.types import CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
# from aiogram.dispatcher.filters import Text
import keyboards as key
from keyboards import get_kb, get_ikb, get_wmkb, reactivate_kb, recieve_document_kb

from newmongo import *

TOKEN_API = '5956900315:AAGUG4gCptqmSAtuWMO7zG-9itn_Wd8skNM'

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

global num

class UserStates(StatesGroup):
    ACTIVE = State()
    INACTIVE = State() 

class ProfileStatesGroup(StatesGroup):
    name = State()
    surname = State()
    room_number = State()
    phone_number = State()
    password = State()

Action_for_start = """
    Дорбро пожаловать!\nЧтобы привязать ваш аккаунт, нажмите - <b>/Authorize</b>\nЧтобы просмотреть оставшееся количество стирок в этом месяце - нажмите <b>/Display_Info</b>\nЧтобы выбрать машинку - <b>/Order_Washing_Machines</b>"""

Action = """
    Давайте перейдём к записи\nЧтобы просмотреть оставшееся количество стирок в этом месяце - нажмите <b>/Display_Info</b>\nЧтобы выбрать время - <b>/Order_Washing_Machines</b>"""

Action_for_auth_err = """
    Бот остановлен. Вас нет в списках проживающих или вы неправильно ввели данные.\nПопробуйте ввести данные снова.\nЕсли это ошибка в списках, то обратитесь к авторам Бота - @UnnwnKhanZz, @andrew0320"""

Action_for_reset = """
    Вы прервали запись!\nБот приостановлен, для перезапуска нажмите кнопку ниже ↓"""


@dp.message_handler(command = ['Start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer(text = Action_for_start, parse_mode= 'HTML', reply_markup = get_kb())

@dp.message_handler(command = ['Reset_bot'])
async def cmd_reset(message: types.Message) -> None:
    await message.reply(text = Action_for_reset, parse_mode = 'HTML', reply_markup= reactivate_kb)
    await UserStates.INACTIVE.set()

@dp.message_handler(command = ['Reactivate_bot'])
async def cmd_reactivate(message: types.Message) -> None:
    await message.answer('Бот перезапущен')
    await message.answer(text= Action_for_start, parse_mode = 'HTML', reply_markup=get_kb())
    await UserStates.ACTIVE.set()



@dp.message_handler(command = ['Authorize'])
async def authorize_start(message: types.Message) -> None:
    if check_key(["id"], [message.from_user.id]):
        await message.answer("Вы уже подключены, авторизовываться не надо")
        await message.answer(text = Action, parse_mode='HTML')
    else:
        await message.answer("Давайте привяжем вас к вашему аккаунту. Введите ваше имя")
        await ProfileStatesGroup.name.set()




@dp.message_handler(lambda message: not message.text, state=ProfileStatesGroup.name)
async def check_name(message: types.Message):
    await message.reply('Это не имя!')

@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.name)
async def load_name(message: types.Message) -> None:
    if not check_key(["name"], [message.text]):
        await message.answer(text = Action_for_auth_err, parse_mode= 'HTML')
        await dp.bot.stop(message.from_user.id)

    global name
    name = message.text

    if message.text == 'admin':
        await message.answer('Введите пароль')
        await ProfileStatesGroup.password()
    else:
        await message.answer('Теперь отправьте свою фамилию')
        await ProfileStatesGroup.next()


@dp.message_handler(state = ProfileStatesGroup.password)
async def admin_keyboard(message: types.Message) -> None:
    if message.text == '12345':
        await message.answer('Для получения списка записей на сегодня, нажмите кнопку ниже ↓', reply_markup=recieve_document_kb)
    else:
        await message.asnwer('Пароль введён неверно!\nБот приостановлен')
        dp.bot.stop(message.from_user.id)

@dp.message_handler(commands = ['Receive_Document'])
async def document_push(message: types.Message):
    await message.answer('d;dwa') # здесь выгрузка документа


@dp.message_handler(lambda message: not message.text or message.text.isdigit(), state=ProfileStatesGroup.surname)
async def check_surname(message: types.Message):
    await message.reply('Это не фамилия!')

@dp.message_handler(state=ProfileStatesGroup.surname)
async def load_surname(message: types.Message) -> None:
    global name
    if not check_key(["name", "surname"], [name, message.text]):
        await message.answer(text = Action_for_auth_err)
        await dp.bot.stop(message.from_user.id)

    global surname
    surname = message.text

    await message.answer('Введите номер комнаты')
    await ProfileStatesGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 1000 or float(message.text) < 100, state=ProfileStatesGroup.room_number)
async def check_room_number(message: types.Message):
    await message.reply('Введите реальный номер!')

@dp.message_handler(state=ProfileStatesGroup.room_number)
async def load_room_number(message: types.Message) -> None:
    global name, surname
    if not check_key(["name", "surname", "room_num"], [name, surname, message.text]):
        await message.answer(text = Action_for_auth_err)
        await dp.bot.stop(message.from_user.id)

    global room_num
    room_num = message.text

    await message.answer('Введите ваш номер телефона без различных знаков и пробелов')
    await ProfileStatesGroup.next()


@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) < 87000000000 or float(message.text) > 88000000000, state=ProfileStatesGroup.phone_number)
async def check_phone_number(message: types.Message):
    await message.reply('Введите реальный номер!')

@dp.message_handler(state=ProfileStatesGroup.phone_number)
async def load_phone_number(message: types.Message, state: FSMContext) -> None:
    global name, surname, room_num
    add_info(name, surname, room_num, message.text, message.from_user.id)

    await message.answer(text = Action, parse_mode='HTML')
    await state.finish()




@dp.message_handler(commands=['Display_Info'])
async def display_handler(message: types.Message):
    await message.answer(f'Оставшееся количество стирок: {give_user_number_orders(message.from_user.id)}\n')


@dp.message_handler(comamnds = ['Order_Laundry'])
async def order_laundry(message: types.Message):
    if give_user_number_orders(message.from_user.id) <= 0:
        await message.answer('У вас закончились свободные стирки')
    else:
        await bot.send_message(chat_id = message.from_user.id, text='Выберите свободную стиральную машинку для записи', reply_markup=get_wmkb())



@dp.callback_query_handler(text = 'first_wm')
async def first_wm(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id = callback.message.chat.id, message_id = callback.message.message_id, reply_markup = None)
    await callback.message.answer(text = 'Вы выбрали машинку номер 1', reply_markup = get_ikb(1))

    global num
    num = 1

    await callback.answer()

@dp.callback_query_handler(text = 'second_wm')
async def first_wm(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id = callback.message.chat.id, message_id = callback.message.message_id, reply_markup = None)
    await callback.message.answer(text = 'Вы выбрали машинку номер 2', reply_markup = get_ikb(2))

    global num
    num = 2

    await callback.answer()

@dp.callback_query_handler(text = 'third_wm')
async def first_wm(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id = callback.message.chat.id, message_id = callback.message.message_id, reply_markup = None)
    await callback.message.answer(text = 'Вы выбрали машинку номер 3', reply_markup = get_ikb(3))

    global num
    num = 3

    await callback.answer()

@dp.callback_query_handler(text = 'fourth_wm')
async def first_wm(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id = callback.message.chat.id, message_id = callback.message.message_id, reply_markup = None)
    await callback.message.answer(text = 'Вы выбрали машинку номер 4', reply_markup = get_ikb(4))

    global num
    num = 4
    
    await callback.answer()

@dp.callback_query_handler(text = 'fifth_wm')
async def first_wm(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id = callback.message.chat.id, message_id = callback.message.message_id, reply_markup = None)
    await callback.message.answer(text = 'Вы выбрали машинку номер 5', reply_markup = get_ikb(5))

    global num
    num = 5

    await callback.answer()

@dp.callback_query_handler(text = 'sixth_wm')
async def first_wm(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id = callback.message.chat.id, message_id = callback.message.message_id, reply_markup = None)
    await callback.message.answer(text = 'Вы выбрали машинку номер 6', reply_markup = get_ikb(6))

    global num
    num = 6

    await callback.answer()

@dp.callback_query_handler(text = 'seventh_wm')
async def first_wm(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id = callback.message.chat.id, message_id = callback.message.message_id, reply_markup = None)
    await callback.message.answer(text = 'Вы выбрали машинку номер 7', reply_markup = get_ikb(7))

    global num
    num = 7

    await callback.answer()



@dp.callback_query_handler(text = "ninetoten")
async def nine_to_ten_handler(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id = callback.message.chat.id, message_id = callback.message.message_id, reply_markup = None)
    await callback.message.answer(text='Вы зарегистрировались на промежуток 9:00 - 10:10')
    
    number = give_user_number_orders(callback.message.chat.id)
    change_number_orders(callback.message.chat.id, number-1)

    global num
    change_free_time(num, "9.00-10.10", False)

    await callback.answer()

@dp.callback_query_handler(text = "tentoeleven")
async def ten_to_el_handler(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id = callback.message.chat.id, message_id = callback.message.message_id, reply_markup = None)
    await callback.message.answer(text='Вы зарегистрировались на промежуток 10:10 - 11:20')
    
    number = give_user_number_orders(callback.message.chat.id)
    change_number_orders(callback.message.chat.id, number-1)

    global num
    change_free_time(num, "10.10-11.20", False)

    await callback.answer()


@dp.callback_query_handler(text = "eleventotwelve")
async def el_to_twelve_handler(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id = callback.message.chat.id, message_id = callback.message.message_id, reply_markup = None)
    await callback.message.answer(text='Вы зарегистрировались на промежуток 11:20 - 12:30')
    
    number = give_user_number_orders(callback.message.chat.id)
    change_number_orders(callback.message.chat.id, number-1)

    global num
    change_free_time(num, "11.20-12.30", False)

    await callback.answer()


@dp.callback_query_handler(text = "twelvetothirteen")
async def twelve_to_thir_handler(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id = callback.message.chat.id, message_id = callback.message.message_id, reply_markup = None)
    await callback.message.answer(text='Вы зарегистрировались на промежуток 12:30 - 14:00.\nНапоминание: с 13:00 до 14:00 - обеденное время.')
    
    number = give_user_number_orders(callback.message.chat.id)
    change_number_orders(callback.message.chat.id, number-1)

    global num
    change_free_time(num, "12.30-14.00", False)

    await callback.answer()


@dp.callback_query_handler(text = "thirteentofourteen")
async def thir_to_four_handler(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id = callback.message.chat.id, message_id = callback.message.message_id, reply_markup = None)
    await callback.message.answer(text='Вы зарегистрировались на промежуток 14:00 - 15:10')
    
    number = give_user_number_orders(callback.message.chat.id)
    change_number_orders(callback.message.chat.id, number-1)

    global num
    change_free_time(num, "14.00-15.10", False)

    await callback.answer()


@dp.callback_query_handler(text = "fourteentofifteen")
async def four_to_fif_handler(callback: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id = callback.message.chat.id, message_id = callback.message.message_id, reply_markup = None)
    await callback.message.answer(text='Вы зарегистрировались на промежуток 15:10 - 16:20')
    
    number = give_user_number_orders(callback.message.chat.id)
    change_number_orders(callback.message.chat.id, number-1)

    global num
    change_free_time(num, "9.00-10.10", False)

    await callback.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)