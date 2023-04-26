from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
import newmongo

def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/Authorize'))
    kb.add(KeyboardButton('/Display_Info'))
    kb.add(KeyboardButton('/Order_Laundry'))
    kb.add(KeyboardButton('/Cancel_My_Book'))
    kb.add(KeyboardButton('/Reset_Bot'))

    return kb

collecton_ikb = [
                InlineKeyboardButton(text='с 9:00 до 10:10', callback_data='ninetoten'), 
                InlineKeyboardButton(text='с 10:10 до 11:20', callback_data='tentoeleven'),
                InlineKeyboardButton(text='с 11:20 до 12:30', callback_data='eleventotwelve'),
                InlineKeyboardButton(text='с 12:30 до 14:00', callback_data='twelvetothirteen'),
                InlineKeyboardButton(text='с 14:00 до 15:10', callback_data='thirteentofourteen'),
                InlineKeyboardButton(text='с 15:10 до 16:20', callback_data='fourteentofifteen'),
]


collecton_wmkb = [
                InlineKeyboardButton(text='1 машинка, 40 градусов', callback_data='first_wm'), 
                InlineKeyboardButton(text='2 машинка, 40 градусов', callback_data='second_wm'),
                InlineKeyboardButton(text='3 машинка, 60 градусов', callback_data='third_wm'),
                InlineKeyboardButton(text='4 машинка, 40 градусов', callback_data='fourth_wm'),
                InlineKeyboardButton(text='5 машинка, 40 градусов', callback_data='fifth_wm'),
                InlineKeyboardButton(text='6 машинка, 40 градусов', callback_data='sixth_wm'),
                InlineKeyboardButton(text='7 машинка, 40 градусов', callback_data='seventh_wm')
]


recieve_document_kb = ReplyKeyboardMarkup(resize_keyboard = True)
recieve_document_kb.add(KeyboardButton('/Receive_Document'))

reactivate_kb = ReplyKeyboardMarkup(resize_keyboard=True)
reactivate_kb.add(KeyboardButton('/Reactivate_bot'))


def get_wmkb() -> InlineKeyboardMarkup:
    global collecton_wmkb

    wmkb = InlineKeyboardMarkup(row_width=2)

    available = []
    available = newmongo.free_washers()

    for i in range(0, 7):
        if available[i] == True:
            ikb1 = collecton_wmkb[i]
            wmkb.add(ikb1)
        else:
            continue

    return wmkb


def get_ikb(id) -> InlineKeyboardMarkup:
    global collecton_ikb

    ikb = InlineKeyboardMarkup(row_width=2)

    available = []
    available = newmongo.free_time(int(id))

    for i in range(0, 6):
        if available[i] == True:
            ikb1 = collecton_ikb[i]
            ikb.add(ikb1)
        else:
            continue

    return ikb