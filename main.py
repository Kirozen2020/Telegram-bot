import telebot
import random
from datetime import datetime

from telebot import types

bot = telebot.TeleBot(TOKEN)

name = ""
surname = ""
age = 0

element = ""
nameElement = ""
myList = {}

@bot.message_handler(commands = ['start'])
def welcome(message):
    global name, surname, age, element, nameElement, myList

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲Random number")
    item2 = types.KeyboardButton("How are you today?")

    name = ""
    surname = ""
    age = 0

    element = ""
    nameElement = ""
    myList = {}

    markup.add(item1, item2)

    bot.send_message(message.chat.id, f"Hello, my name is Anonim bot!\nPlease do check in!('/chack_in)", reply_markup=markup)


@bot.message_handler(commands=['chack_in'])
def register(message):
    global age
    age = 0
    bot.send_message(message.chat.id, "Hey! Let's get acquainted! What's your name?")
    bot.register_next_step_handler(message, reg_name)


def reg_name(message):
    global name
    name = message.text
    bot.send_message(message.chat.id, "Waht you last name? ")
    bot.register_next_step_handler(message, reg_surname)


def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.chat.id, "How old are you? ")
    bot.register_next_step_handler(message, reg_age)


def reg_age(message):
    global age, name, surname
    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.chat.id, "Enter with numbers please!")
    bot.send_message(message.chat.id, f"your name is: {name} {surname}, and you are {age} years old")
    bot.send_message(message.chat.id, "If you see mistake -> do chack in another time (/chackin)")


@bot.message_handler(commands = ['time'])
def time_now(message):
    corect_time = datetime.now()
    haur = corect_time.hour
    haur = haur + 2
    minut = corect_time.minute
    if haur < 10:
        if minut < 10 and minut <= 60:
            bot.send_message(message.chat.id, f"Time now is 0{haur}:0{minut}")
        elif minut >= 10 and minut <= 60:
            bot.send_message(message.chat.id, f"Time now is 0{haur}:{minut}")
    elif haur >= 10:
        if minut < 10 and minut <= 60:
            bot.send_message(message.chat.id, f"Time now is {haur}:0{minut}")
        elif minut >= 10 and minut <= 60:
            bot.send_message(message.chat.id, f"Time now is {haur}:{minut}")


@bot.message_handler(commands = ['date'])
def date_now(message):
    corect_time = datetime.now()
    day = corect_time.day
    month = corect_time.month
    year = corect_time.year
    d = corect_time.strftime("%A %B, %Y")
    bot.send_message(message.chat.id, f"{d}\n{day}/{month}/{year}")


@bot.message_handler(commands=['add_to_list'])
def addList(message):
    bot.send_message(message.chat.id, "What the name of the element?")
    bot.register_next_step_handler(message, getNameElement)


def getNameElement(message):
    global nameElement, myList
    nameElement = message.text
    bot.send_message(message.chat.id, "What the element")
    bot.register_next_step_handler(message, getElement)


def getElement(message):
    global element, myList, nameElement
    element = message.text
    myList[nameElement] = element
    bot.send_message(message.chat.id, "appended!\n"
                                      "if you want to appent another element: /add_to_list")


@bot.message_handler(commands=['delete_element'])
def delete_element(message):
    bot.send_message(message.chat.id, "This is you'r list")
    if len(myList)==0:
        bot.send_message(message.chat.id, "if you see this, the list is clear")
    else:
        bot.send_message(message.chat.id, f"{myList}")
    bot.send_message(message.chat.id, "What the name of the element?")
    bot.register_next_step_handler(message, delit)

def delit(message):
    global myList
    nel = message.text
    if nel in myList:
        myList.pop(nel)
    bot.send_message(message.chat.id, "deleted")

@bot.message_handler(commands=['print_list'])
def printList(message):
    if len(myList)==0:
        bot.send_message(message.chat.id, "if you see this, the list is clear")
    else:
        bot.send_message(message.chat.id, f"{myList}")


@bot.message_handler(commands=['clear_list'])
def clearList(message):
    global myList
    myList.clear()
    bot.send_message(message.chat.id, "The list is clear now")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Command '/time' - send you the time now\n"
                                      "Command '/date' - send you the date now\n"
                                      "Command '/add_to_list' - add 1 new element to list\n"
                                      "Command '/print_list' - send you all element in the list\n"
                                      "Command '/clear_list' - clear the list\n"
                                      "Command '/chack_in' - creat new persone (name, last name and age)\n"
                                      "Command '/delete_element - delete specific element from the list")




@bot.message_handler(content_types = ['text'])
def lalala(message):
    # bot.send_message(message.chat.id, message.text)
    if message.chat.type == 'private':
        if message.text == '🎲Random number':
            bot.send_message(message.chat.id, str(random.randint(0,100)))
        elif message.text == 'How are you today?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Good", callback_data='good')
            item2 = types.InlineKeyboardButton("So so", callback_data='bad')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'exelent, How you? ', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "I don't knew what to say\nI am don't have command like this")


@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    try:
        if call.data == 'good':
            bot.send_message(call.message.chat.id, "It's good, I am happy for you😀")
        elif call.data == 'bad':
            bot.send_message(call.message.chat.id, "It happens, don't be sad😥")

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="How are you today?", reply_markup=None)

        bot.answer_callback_query(shat_id = call.message.chat.id, show_alert=False, text="Test")

    except Exception as e:
        print(repr(e))


bot.polling(none_stop = True)