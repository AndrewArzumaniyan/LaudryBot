from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
import mongo

def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/Authorize'))
    kb.add(KeyboardButton('/Display_info'))
    kb.add(KeyboardButton('/Order_laundry'))
    kb.add(KeyboardButton('/Cancel'))

    
    return kb

collecton_ikb = [
                InlineKeyboardButton(text='с 9:00 до 10:10', callback_data='ninetoten'), 
                InlineKeyboardButton(text='с 10:10 до 11:20', callback_data='tentoeleven'),
                InlineKeyboardButton(text='с 11:20 до 12:30', callback_data='eleventotwelve'),
                InlineKeyboardButton(text='с 12:30 до 13:40', callback_data='twelvetothirteen'),
                InlineKeyboardButton(text='с 13:40 до 14:50', callback_data='thirteentofourteen'),
                InlineKeyboardButton(text='с 14:50 до 16:00', callback_data='fourteentofifteen'),
                InlineKeyboardButton(text='с 16:00 до 17:00', callback_data='fifteentosixteen')
]


collecton_wmkb = [
                InlineKeyboardButton(text='1 машинка, 40 градусов', callback_data='first_wm'), 
                InlineKeyboardButton(text='2 машинка, 40 градусов', callback_data='second_wm'),
                InlineKeyboardButton(text='3 машинка, 60 градусов', callback_data='third_wm'),
                InlineKeyboardButton(text='4 машинка, 40 градусов', callback_data='fourth_wm'),
                InlineKeyboardButton(text='5 машинка, 40 градусов', callback_data='fifth_wm'),
                InlineKeyboardButton(text='6 машинка, 40 градусов', callback_data='sixth_wm'),
                InlineKeyboardButton(text='7 машинка, 40 градусов', callback_data='seven_wm')
]


recieve_document_kb = ReplyKeyboardMarkup(resize_keyboard = True)
recieve_document_kb.add(KeyboardButton('/Receive_Document'))

reactivate_kb = ReplyKeyboardMarkup(resize_keyboard=True)
reactivate_kb.add(KeyboardButton('/Reactivate_bot'))


def get_wmkb() -> InlineKeyboardMarkup:
    global collecton_wmkb

    wmkb = InlineKeyboardMarkup(row_width=2)

    available = []
    available = mongo.available_time_bool()

    for i in range(0, 7):
        if available[i] == True:
            ikb1 = collecton_wmkb[i]
            wmkb.add(ikb1)
        else:
            continue

    return wmkb


def get_ikb() -> InlineKeyboardMarkup:
    global collecton_ikb

    ikb = InlineKeyboardMarkup(row_width=2)

    available = []
    available = mongo.available_time_bool()

    for i in range(0, 7):
        if available[i] == True:
            ikb1 = collecton_ikb[i]
            ikb.add(ikb1)
        else:
            continue

    return ikb