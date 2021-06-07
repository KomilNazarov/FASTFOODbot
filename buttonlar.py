from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

"""                     BUTTONLAR                      """


def buttons():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button1 = types.KeyboardButton(text="👀 Barcha mahsulotlar ro'yxati")
    button2 = types.KeyboardButton(text="✅ Tanlangan mahsulotlar")
    button3 = types.KeyboardButton(text="🛒 Savatdagi mahsulotlar")
    keyboard.add(button1, button2, button3)
    return keyboard


"""              INLINE BUTTONLAR                       """


def product_buttons():
    reply_markup = InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton(text="🛒 XARID QILISH", callback_data="xarid")
    button2 = types.InlineKeyboardButton(text="✅ TANLANGANGA QO'SHISH", callback_data="tanlash")
    reply_markup.add(button1, button2)
    return reply_markup


"""               RAQAMLAR                              """


def sonlar():
    sonlar = types.InlineKeyboardMarkup(row_width=3)
    bir = types.InlineKeyboardButton(text="1", callback_data=1)
    ikki = types.InlineKeyboardButton(text="2", callback_data=2)
    uch = types.InlineKeyboardButton(text="3", callback_data="3")
    tort = types.InlineKeyboardButton(text="4", callback_data="4")
    besh = types.InlineKeyboardButton(text="5", callback_data="5")
    olti = types.InlineKeyboardButton(text="6", callback_data="6")
    yetti = types.InlineKeyboardButton(text="7", callback_data="7")
    sakkiz = types.InlineKeyboardButton(text="8", callback_data="8")
    toqqiz = types.InlineKeyboardButton(text="9", callback_data="9")
    sonlar.add(InlineKeyboardButton(text="Ko'proq xarid qilish", callback_data="ko'proq"))
    sonlar.add(bir, ikki, uch, tort, besh, olti, yetti, sakkiz, toqqiz, )

    return sonlar


"""             SAVATNI TOZALOVCHI BUTTON       """


def remove_button():
    re_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    re_button.add(text="❌ savatni tozalash")
    return re_button