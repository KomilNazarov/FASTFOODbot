import re
import telebot
import json
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

token = "1731457221:AAHFz9tnIA6xQYWqZXD9O9I7sw4QXj9LOI0"


bot = telebot.TeleBot(token=token)

savatdagi_mahsulotlar, tallangan_mahsulotlar = [], []  # -- ko'p marta qo'shish uchun

savatdagi_mahsulotlar_royxati, tallangan_mahsulotlar_royxati = [], []  # bir marta qushish uchun

with open("products.json", 'r') as f:
    product = json.load(f)
user_cart = {}


def product_keyboard(pro_name):
    reply_markup = InlineKeyboardMarkup(row_width=3)
    reply_markup.add(*[
        InlineKeyboardButton(text='-', callback_data=f'decrement:{pro_name}'),
        InlineKeyboardButton(text='1', callback_data='pass'),
        InlineKeyboardButton(text='+', callback_data=f'increment:{pro_name}'),
    ])
    reply_markup.add(InlineKeyboardButton(text="sd", callback_data="sd"))
    return reply_markup

@bot.message_handler(commands=['start'])
def send_welkome(message):
    name = message.from_user.first_name
    msg = f'Salom {name} VIKI fast food botga xush kelibsiz!\nMaxsulot qidirish uchun nomini kiriting'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    button1 = types.KeyboardButton(text="👀 Barcha mahsulotlar ro'yxati")
    button2 = types.KeyboardButton(text="✅ Tanlangan mahsulotlar")
    button3 = types.KeyboardButton(text="🛒 Savatdagi mahsulotlar")
    keyboard.add(button1, button2, button3)
    bot.send_message(chat_id=message.chat.id, text=msg, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def all_message_handler(message):
    request_text = message.text
    global product

    """    barcha maxsulotlarni kurish  """
    if request_text == "👀 Barcha mahsulotlar ro'yxati":
        for pro in product:
            chat_id = message.chat.id
            nomi = pro['nomi']
            narxi = pro['narxi']
            rasmi = pro['rasmi']
            caption = "{}\n{}".format(nomi, narxi)
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton(
                text="🛒 Savatga qo'shish",
                callback_data="Savatga_qo'shish:{}".format(nomi))
            button2 = types.InlineKeyboardButton(
                text="✅ Tallanganga qo'shish",
                callback_data="Tallanganga_qo'shildi:{}".format(nomi))
            keyboard.add(button1, button2)
            bot.send_photo(chat_id=chat_id, photo=rasmi, caption=caption, reply_markup=keyboard)

    elif request_text.lower() == "🛒 savatdagi mahsulotlar":
        bot.send_message(message.chat.id, 'Savatdagi maxsulotlar soraldi ')
        savat = ""
        jami_summa = 0
        for mahsulot in savatdagi_mahsulotlar:
            savatdagi_mahsulotlar_soni = mahsulot.get("soni")
            summa = mahsulot.get("narxi")
            for product in product:
                if product.get("nomi") == mahsulot:
                    summa = product.get("narxi")
            jami_summa += summa * savatdagi_mahsulotlar_soni
            savat += "{} x {} = {} so'm\n".format(
                mahsulot.get("nomi"),
                savatdagi_mahsulotlar_soni,
                summa * savatdagi_mahsulotlar_soni
            )
        savat += "\nUmumiy so'mma: {} so'm".format(jami_summa)
        if jami_summa == 0:
            savat = "Sizning savatingiz bo'sh\n \nUmumiy narx: {}".format(jami_summa)
        butoonlar_ruyhati = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text="◀️Orqaga")
        for mahsulot in savatdagi_mahsulotlar:
            mahsulot_button = types.KeyboardButton("❌ {}".format(mahsulot.get("nomi"))
                                                   )
            butoonlar_ruyhati.add(mahsulot_button)
        butoonlar_ruyhati.add(button1)
        bot.send_message(message.chat.id, text=savat, reply_markup=butoonlar_ruyhati)

    elif request_text.lower() == "◀️orqaga":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton(text="🛒 Savatdagi mahsulotlar")
        button2 = types.KeyboardButton(text="✅ Tallangan mahsulotlar")
        button3 = types.KeyboardButton(text="👀 Barcha mahsulotlar ro'yxati")
        keyboard.add(button1, button2, button3)
        bot.send_message(message.chat.id, text="orqaga qaytdim", reply_markup=keyboard)

    elif request_text == "✅ Tallangan mahsulotlar":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton(text="◀️Orqaga")

        text = ""
        full_price = 0
        for number_product, mahsulot in enumerate(tallangan_mahsulotlar_royxati):
            button = types.KeyboardButton(text="❎ {}".format(mahsulot))
            keyboard.add(button)

            count = tallangan_mahsulotlar.count(mahsulot)
            price = 0
            for product in product:
                if product.get("nomi") == mahsulot:
                    price = int(product.get("narxi"))
            full_price += price * count
            text += "{}. {}\n".format(
                number_product + 1, mahsulot, count, price * count)

        text += 'Jami summa: {}'.format(full_price)
        if full_price == 0:
            text = "Hali mahsulot tallanmagan"
        keyboard.add(button1)
        bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
    else:
        pass
        found_product = 0
        for pro in product:
            if request_text.lower() in pro['nomi'].lower():
                found_product += 1
                chat_id = message.chat.id
                nomi = pro['nomi']
                narxi = pro['narxi']
                rasmi = pro['rasmi']
                caption = "{}\n{}".format(nomi, narxi)

                keyboard = types.InlineKeyboardMarkup(row_width=2)
                button1 = types.InlineKeyboardButton(
                    text="🛒 Savatga qo'shish",
                    callback_data="Savatga_qo'shish:{}".format(nomi))

                button2 = types.InlineKeyboardButton(
                    text="✅ Tallanganga qo'shish",
                    callback_data="Tallanganga_qo'shildi:{}".format(nomi))
                keyboard.add(button1, button2)
                bot.send_photo(chat_id=chat_id, photo=rasmi, caption=caption, reply_markup=keyboard)
        if found_product == 0:
            bot.send_message(chat_id=message.chat.id, text="Mahsulot topilmadi")



@bot.callback_query_handler(func = lambda  c :True)
def callback_message(callback):
    callback_data, pro_name = callback.data.split(':')
    print(callback.data)
    if callback_data == "Savatga_qo'shish":
        if user_cart.get(callback.from_user.id, None):
            user_cart[callback.from_user.id]['cart'].append({'product_id': pro_name, 'quantity': 1})
            print(user_cart)
        else:
            user_cart[callback.from_user.id] = {'cart': [{'product_id': pro_name, 'quantity': 1}]}
        reply_murkup = product_keyboard(pro_name)

        bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id, reply_markup=reply_murkup)
    elif callback_data == "increment":
        u_cart = user_cart[callback.from_user.id]
        for cart in u_cart['cart']:
            if cart['product_id'] == pro_name:
                cart['quantity'] += 1
                reply_markup = product_keyboard(pro_name)
                bot.edit_message_reply_markup(
                    callback.from_user.id,
                    callback.message.message_id,
                    reply_markup=reply_markup
                )
                break
    elif callback_data == "decrement":
        u_cart = user_cart[callback.from_user.id]
        for index, cart in enumerate(u_cart['cart']):
            if cart['product_id'] == pro_name:
                cart['quantity'] -= 1
                if cart['quantity'] > 0:
                    reply_markup = product_keyboard(pro_name)
                    bot.edit_message_reply_markup(
                        callback.from_user.id,
                        callback.message.message_id,
                        reply_markup=reply_markup
                    )
                else:
                    u_cart['cart'].pop(index)
                    reply_markup = InlineKeyboardMarkup(row_width=3)
                    reply_markup.add(*[
                        InlineKeyboardButton(text="🛒 Savatga qo'shish",
                                             callback_data="Savatga_qo'shish:{}".format(pro_name)),
                        InlineKeyboardButton(text="✅ Tallangan mahsulotlar",
                                             callback_data="Tallanganga_qo'shildi:{}".format(pro_name))])
                    bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id,
                                                  reply_markup=reply_markup)
                break


bot.polling()
