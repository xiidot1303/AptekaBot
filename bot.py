from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ChatAction
import xlrd
import os
from conversationList import GLOBAL_NAME, SELECT_DRUGS, SUPERADMIN, UPDATE_EXCEL, START, EDIT_ABOUT_US, UPDATE_ABOUT_US, WRITE_NAME, SEND_PHONE
import sqlite3
from functions import sort_percent_grow, sort_price_grow, sort_price_wane, sort_percent_wane

def forward(update, context):
    print(update.message.forward_from)


def issuperadmin(id):
    if id == superadmin:
        return True
    else:
        return False
superadmin = 206261493
def start(update, context):
    
    admins = []
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM admins ")
    for i in c.fetchall():

        admins.append(i[0]) 
    
    conn.commit()
    conn.close()   
    if update.message.chat.id == superadmin:
        update.message.reply_text("Вас приветствует главный админ панель бота", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
        
        return SUPERADMIN
    elif update.message.chat.id in admins:
        update.message.reply_text("Вас приветствует админ панель бота", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт']], resize_keyboard=True))
        return SUPERADMIN
    else:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id={}".format(update.message.chat.id))
        user = c.fetchone()
        if user:
            update.message.reply_text("Вас приветствует бот по поиску лекарств о компании название компании", reply_markup=ReplyKeyboardMarkup(keyboard=[['Поиск лекарств🔎'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт'], ['Настройки⚙️']], resize_keyboard=True))
            conn.commit()
            conn.close()
        else:
            c.execute("INSERT INTO users VALUES ({}, 'x', 'x')".format(update.message.chat.id))
            conn.commit()
            conn.close()
            update.message.reply_text('Напишите свое имя')
            return WRITE_NAME

    conn.commit()
    conn.close()   

#registr
def write_name(update, context):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""UPDATE users SET name = '{}' WHERE id={} """.format(update.message.text, update.message.chat.id))

    conn.commit()
    conn.close()
    i_contact = KeyboardButton(text='отправить ', request_contact=True)
    update.message.reply_text('Хорошо, отправьте номер телефона', reply_markup=ReplyKeyboardMarkup([[i_contact]], resize_keyboard=True))
    return SEND_PHONE

def send_phone(update, context):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""UPDATE users SET phone_number = '{}' WHERE id={} """.format(str(update.message.contact.phone_number), update.message.chat.id))

    conn.commit()
    conn.close()
    update.message.reply_text("Вас приветствует бот по поиску лекарств о компании название компании", reply_markup=ReplyKeyboardMarkup(keyboard=[['Поиск лекарств🔎'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт'], ['Настройки⚙️']], resize_keyboard=True))
    return ConversationHandler.END


def global_name(update, context):
    bot = context.bot
    text = update.message.text 
    if text == 'Назад':
        update.message.reply_text("Главное меню", reply_markup=ReplyKeyboardMarkup(keyboard=[['Поиск лекарств🔎'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт'], ['Настройки⚙️']], resize_keyboard=True))
        return ConversationHandler.END
    else:
        bot.send_chat_action(chat_id=update.message.chat.id, action=ChatAction.TYPING)
        p = os.listdir()
        for i in p:
            if i[-3::] == 'xls' or i[-4::] == 'xlsx':
                path = i
                break
        
        name = update.message.text
        workbook = xlrd.open_workbook('{}'.format(path))
        worksheet = workbook.sheet_by_index(0)
        c = 0
        r = []
        for i in worksheet.col_values(0):
            if name.lower() in i.lower():
                bot.send_chat_action(chat_id=update.message.chat.id, action=ChatAction.TYPING)
                r.append(c)
            c += 1
        c = 0
        if not r:
            for i in worksheet.col_values(1):
                
                
                try:
                    if name.lower() == i.lower():
                        bot.send_chat_action(chat_id=update.message.chat.id, action=ChatAction.TYPING)

                        r.append(c)
                except:
                    wefwefw = 9
                c += 1
        items = []
        texts = []
        if not r:
            mrk = [[KeyboardButton(text='Назад')]]
            update.message.reply_text('Ничего не найдено, попробуйте еще раз', reply_markup=ReplyKeyboardMarkup(mrk, resize_keyboard=True, one_time_keyboard=True))
            return GLOBAL_NAME
        else:
            for i in r:
                w = worksheet.row_values(i)
                if not w[0] in texts:
                    texts.append(w[0])
                    items.append([KeyboardButton(text=w[0])])
            items.append([KeyboardButton(text='Назад'), KeyboardButton(text='Главная')])
            update.message.reply_text('Пожалуйста, выберите лекарство из предоставленного списка.', reply_markup=ReplyKeyboardMarkup(items, resize_keyboard=True, one_time_keyboard=True))
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute("SELECT * FROM access_to_find WHERE id={} ".format(update.message.chat.id))
            n = c.fetchone()[2]
            c.execute("""UPDATE access_to_find SET chance = {} WHERE id={} """.format(int(n)-1, update.message.chat.id))
            conn.commit()
            conn.close()
            return SELECT_DRUGS
    

def select_drugs(update, context):
    bot = context.bot
    name = update.message.text
    if name == 'Главная':
        update.message.reply_text("Главное меню", reply_markup=ReplyKeyboardMarkup(keyboard=[['Поиск лекарств🔎'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт'], ['Настройки⚙️']], resize_keyboard=True))
        return ConversationHandler.END
    if name == 'Назад':
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM access_to_find WHERE id={} ".format(update.message.chat.id))
        f = update.message.date
        fetchone = c.fetchone()
        d = ''
        for x in str(f):
            if x == ' ':
                break
            else:
                d += x

        if not fetchone:

            c.execute("INSERT INTO access_to_find VALUES ({}, '{}', 5)".format(update.message.chat.id, d))
            conn.commit()
            update.message.reply_text('Введите название лекарства, а наш бот подскажет Вам возможные варианты:\n\nПример: анальгин\n(Минимум 3 символа)', reply_markup = ReplyKeyboardMarkup(keyboard=[['Назад']], resize_keyboard=True))
            conn.close()
            return GLOBAL_NAME
        else:
            date = fetchone[1]
            chance = fetchone[2]
            y, m, last_day = date.split('-')
            y1, m1, current_day = d.split('-')
            print(last_day, current_day)
            if last_day == current_day:

                if int(chance) <= 0:
                    

                    update.message.reply_text('Лимит на ежедневный поиск 5 раз\nВы использовали все это', reply_markup=ReplyKeyboardMarkup(keyboard=[['Поиск лекарств🔎'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт'], ['Настройки⚙️']], resize_keyboard=True))
                    return ConversationHandler.END
                else:
                    update.message.reply_text('Введите название лекарства, а наш бот подскажет Вам возможные варианты:\n\nПример: анальгин\n(Минимум 3 символа)', reply_markup = ReplyKeyboardMarkup(keyboard=[['Назад']], resize_keyboard=True))
                    conn.close()
                    return GLOBAL_NAME
            else:
                c.execute("""UPDATE access_to_find SET last_date = '{}' WHERE id={} """.format(current_day, update.message.chat.id))
                c.execute("""UPDATE access_to_find SET chance = 5 WHERE id={} """.format(update.message.chat.id))
                conn.commit()
                update.message.reply_text('Введите название лекарства, а наш бот подскажет Вам возможные варианты:\n\nПример: анальгин\n(Минимум 3 символа)', reply_markup = ReplyKeyboardMarkup(keyboard=[['Назад']], resize_keyboard=True))
                conn.close()
                return GLOBAL_NAME

    else:
        bot.send_chat_action(chat_id=update.message.chat.id, action=ChatAction.TYPING)
        p = os.listdir()
        for i in p:
            if i[-3::] == 'xls' or i[-4::] == 'xlsx':
                path = i
                break
        workbook = xlrd.open_workbook('{}'.format(path))

        worksheet = workbook.sheet_by_index(0)

        c = 0
        r = []
        for i in worksheet.col_values(0):
            if i == name:
                r.append(c)
            c += 1

        results = ""
        w = []
        for i in r:
            col = worksheet.row_values(i)
            w.append(col)
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM sort WHERE id = {} ".format(update.message.chat.id))
        obj = c.fetchone()
        if obj[1] == 'цене':
            
            if obj[2] == 'возрастание':
                w = sort_price_grow(w)
            elif obj[2] == 'убывание':
                w = sort_price_wane(w)
        elif obj[1] == 'процентам':
            
            if obj[3] == 'возрастание':
                w = sort_percent_grow(w)
            elif obj[3] == 'убывание':
                w = sort_percent_wane(w)
        print(w)
        c.execute("SELECT * FROM date ")
        f = c.fetchone()[0]
        
        d = ''
        for x in str(f):
            if x == ' ':
                break
            else:
                d += x
        all = w
        min = 10000000000000000000000000.0
        max = 0

        for w in all:
            if w[4] == 0:
                w[4] = 'ожидаемый'
            if max < w[4]:
                max = w[4]
            if min > w[4]:
                min = w[4]
            results += '\nНазвания: ' + w[0] + '\nПроизводитель: ' + w[9] + '({})'.format(w[10]) + '\nАдрес:' + find_address(w[8]) + '\nЦена сум: ' + str(w[4]) + '\nЦена в долларах США: ' + str(w[5]) + '\nЦена в ЕВРО: ' + str(w[6]) + '\nТелефон: '+ find_phone(w[8]) + '\n\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n'
        min_and_max = '↗️ Максимальная цена: {} сум.\n↘️ Минимальная цена:  {}} сум.'.format(str(max), str(min))

        results = 'Дата загрузки прайса: ' + d + '\n' + results
        bot.send_message(update.message.chat.id, results)
        bot.send_message(update.message.chat.id, min_and_max)
        return SELECT_DRUGS        
    

def find_address(title):

    p = os.listdir()
    for i in p:
        if i[-3::] == 'xls' or i[-4::] == 'xlsx':
            path = i
            break
    workbook = xlrd.open_workbook('{}'.format(path))

    worksheet = workbook.sheet_by_index(1)

    c = 0
    r = []
    for i in worksheet.col_values(1):
        
        if i[0:len(title)].lower() == title.lower():
            w = worksheet.row_values(c)
                 
            return w[3]
            break
        c += 1
    else:
        return 'Не указан'

def find_phone(title):
    print('find_phone')
    p = os.listdir()
    for i in p:
        if i[-3::] == 'xls' or i[-4::] == 'xlsx':
            path = i
            break
    workbook = xlrd.open_workbook('{}'.format(path))

    worksheet = workbook.sheet_by_index(1)

    c = 0
    r = []
    for i in worksheet.col_values(1):
        
        if i[0:len(title)].lower() == title.lower():
            w = worksheet.row_values(c)
            
            return w[2]
            break
        c += 1
    else:
        return 'Не указан'



def doc(update, context):

    bot = context.bot
    doc = bot.get_file(update.message.document.file_id)
    doc.download(update.message.document.file_name)
    
    p = os.listdir()
    for i in p:
        if i[-3::] == 'xls' or i[-4::] == 'xlsx':
            path = i
            break
    

def update_excel(update, context):
    if not update.message.text == None:
        if issuperadmin(update.message.chat.id):
            update.message.reply_text("главный админ панель бота", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
        else:
            update.message.reply_text("админ панель бота", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт']], resize_keyboard=True))
        return SUPERADMIN    
    else:
        p = os.listdir()
        for i in p:
            if i[-3::] == 'xls' or i[-4::] == 'xlsx':
                path = i
                break
        os.remove(path)
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("""UPDATE date SET datetime = '{}' """.format(str(update.message.date)))
        conn.commit()
        conn.close()
        bot = context.bot
        doc = bot.get_file(update.message.document.file_id)
        doc.download(update.message.document.file_name)
        if issuperadmin(update.message.chat.id):
            update.message.reply_text("главный админ панель бота", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
        else:
            update.message.reply_text("админ панель бота", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт']], resize_keyboard=True))
        return SUPERADMIN

def cancel(update, context):
    print('done')


