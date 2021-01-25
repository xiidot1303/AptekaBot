from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ChatAction

import os
from conversationList import GLOBAL_NAME, SELECT_DRUGS, SUPERADMIN, UPDATE_EXCEL, START, EDIT_ABOUT_US, UPDATE_ABOUT_US, WRITE_NAME, SEND_PHONE
import sqlite3
from functions import sort_percent_grow, sort_price_grow, sort_price_wane, sort_percent_wane
import pandas as pd

from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

superadmin = os.environ.get('SUPERADMIN')

def forward(update, context):
    print(update.message.forward_from)


def issuperadmin(id):
    
    if id == int(superadmin):
        return True
    else:
        return False

def start(update, context):
    
    admins = []
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM admins ")
    for i in c.fetchall():

        admins.append(i[0]) 
    
    conn.commit()
    conn.close()   
    if update.message.chat.id == int(superadmin):
        update.message.reply_text("Вас приветствует главный админ панель бота", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
        
        return SUPERADMIN
    elif update.message.chat.id in admins:
        update.message.reply_text("Вас приветствует админ панель бота", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт']], resize_keyboard=True))
        return SUPERADMIN
    else:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM sort WHERE id = {} ".format(update.message.chat.id))
        obj = c.fetchall()
        if not obj:
            c.execute("INSERT INTO sort VALUES ({}, 'цене', 'возрастание', 'возрастание')".format(update.message.chat.id))
            conn.commit()



        c.execute("SELECT * FROM users WHERE id={}".format(update.message.chat.id))
        user = c.fetchone()
        if user:
            update.message.reply_text("Вас приветствует бот по поиску лек. средств и изделий медицинского назначения у фарм. дистрибьюторов и отечественных фарм. производителей", reply_markup=ReplyKeyboardMarkup(keyboard=[['Поиск лекарств🔎'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт'], ['Настройки⚙️']], resize_keyboard=True))
            conn.commit()
            conn.close()
        else:
            c.execute("INSERT INTO users VALUES ({}, 'x', 'x')".format(update.message.chat.id))
            conn.commit()
            conn.close()
            update.message.reply_text('Напишите свое имя')
            return WRITE_NAME


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
    if update.message.contact == None or not update.message.contact:
        c.execute("""UPDATE users SET phone_number = '{}' WHERE id={} """.format(str(update.message.text), update.message.chat.id))
    else:
        c.execute("""UPDATE users SET phone_number = '{}' WHERE id={} """.format(str(update.message.contact.phone_number), update.message.chat.id))

    conn.commit()
    conn.close()
    update.message.reply_text("Вас приветствует бот по поиску лек. средств и изделий медицинского назначения у фарм. дистрибьюторов и отечественных фарм. производителей", reply_markup=ReplyKeyboardMarkup(keyboard=[['Поиск лекарств🔎'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт'], ['Настройки⚙️']], resize_keyboard=True))
    return ConversationHandler.END


def global_name(update, context):
    bot = context.bot
    text = update.message.text 
    if text == 'Назад':
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM list_after_search WHERE id={}".format(update.message.chat.id))
        for i in c.fetchall():
            c.execute("DELETE FROM list_after_search WHERE id={} ".format(update.message.chat.id))
        conn.commit()
        conn.close()
        update.message.reply_text("Главное меню", reply_markup=ReplyKeyboardMarkup(keyboard=[['Поиск лекарств🔎'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт'], ['Настройки⚙️']], resize_keyboard=True))
        return ConversationHandler.END
    else:
        bot.send_chat_action(chat_id=update.message.chat.id, action=ChatAction.TYPING)
        p = os.listdir()
        for i in p:
            if i[-3::] == 'xls' or i[-4::] == 'xlsx':
                path = i
                break
        
        name = update.message.text.lower()
        df = pd.read_excel('{}'.format(path), sheet_name=0)
        
        if 'е' in name:
            name = name.replace('е', '(е|ё)')
        if 'ы' in name:
            name = name.replace('ы', '(ы|и)')
        if 'а' in name:
            name = name.replace('а', '(а|о)')
        if 'о' in name:
            name = name.replace('о', '(а|о)')
            if 'а|(а|о)' in name:
                name = name.replace('а|(а|о)', 'а|о')
        if 'и' in name:
            name = name.replace('и', '(и|ы)')
            if 'ы|(и|ы)' in name:
                name = name.replace('ы|(и|ы)', 'ы|и')
        if 'у' in name:
            name = name.replace('у', '(ю|у)')
        if 'с' in name:
            name = name.replace('с', '(ц|с)')
        if '-' in name:
            name = name.replace('-', '(-)?')
        if ' ' in name:
            name = name.replace(' ', '[-, ]?')
        if 'ш' in name:
            name = name.replace('ш', '(-)?(щ|ш)(-)?')
        if 'д' in name:
            name = name.replace('д', 'д(-)?')
        if 'н' in name:
            name = name.replace('н', 'н(-)?(н)?')
        if 'л' in name:
            name = name.replace('л', 'л(л)?')
        if '1' in name or '2' in name or '3' in name or '4' in name or '5' in name or '6' in name or '7' in name or '8' in name or '9' in name:
            numbers = '123456789'
            for n in name:
                if n in numbers:
                    name = name.replace(n, '[-, ]?{}[-, ]?'.format(n))
        df1 = df[(df[df.columns[0]].str.lower().str.contains(r'^(?!a-z){}( )|([-, ,\W,:space:]){}( )'.format(name.lower(), name.lower()), na=False, regex=True))]
        if df1.empty:
            df1 = df[(df[df.columns[1]].str.lower().str.contains(r'{}'.format(name.lower()), na=False, regex=True))]
        items = []
        texts = []
        l = df1[df1.columns[0]]
        for i in l:
            if not i in texts:
                texts.append(i)
                if '`' in i:
                    i = i.replace('`', ' ')
                items.append([InlineKeyboardButton(text=i, callback_data=i)])
        if len(items) == 0:
            
            update.message.reply_text('Данного препарата нет в наших списках. Пожалуйста, введите другое название')
            return GLOBAL_NAME
        else:
        
            update.message.reply_text('Пожалуйста, выберите лекарство из предоставленного списка.', reply_markup=InlineKeyboardMarkup(items, resize_keyboard=True))
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute("SELECT * FROM access_to_find WHERE id={} ".format(update.message.chat.id))
            n = c.fetchone()[2]
            c.execute("""UPDATE access_to_find SET chance = {} WHERE id={} """.format(int(n)-1, update.message.chat.id))
            conn.commit()
            for i in df1.values.tolist():
                c.execute("SELECT * FROM list_after_search WHERE id={} AND zero='{}' AND nine='{}' AND eight='{}' ".format(update.message.chat.id, i[0], i[9], i[8]))
                if not c.fetchone():
                    if i[4] == 'догов.':
                        i[4] = 1
                    elif i[4] == 'ожидаемый':
                        i[4] = 0
                    if '`' in i[0]:
                        i[0] = i[0].replace('`', ' ')


                    c.execute("INSERT INTO list_after_search VALUES ({}, '{}', '{}','{}','{}',{},'{}','{}','{}','{}','{}','{}') ".format(update.message.chat.id,*i))
            conn.commit()            
            conn.close()
            return GLOBAL_NAME
    

def select_drugs(update, context):
    update = update.callback_query
    bot = context.bot
    name = update.data
    
    bot.send_chat_action(chat_id=update.message.chat.id, action=ChatAction.TYPING)
 
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM message WHERE id={} ".format(update.message.chat.id))
    for i in c.fetchall():
        print(i[1])
        bot.delete_message(update.message.chat.id, i[1])
        c.execute("DELETE FROM message WHERE id={} ".format(update.message.chat.id))
        conn.commit()
    c.execute("SELECT zero, one, two, three, four, five, six, seven, eight, nine, ten FROM list_after_search WHERE zero='{}' ".format(name))
    w = c.fetchall()
    if not w:
        bot.send_message(update.message.chat.id, 'Ошибка! Выберите элемент, показанный в списке')
        return GLOBAL_NAME
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
    
    c.execute("SELECT * FROM date ")
    f = c.fetchone()[0]
    
    d = ''
    for x in str(f):
        if x == ' ':
            break
        else:
            d += x
    all = w
    minn = 10000000000000000000000000.0
    maxn = 0
    results = ''
    n = 0
    for w in all:
        w4 = w[4]
        if int(w4) == 0:
            w4 = 'ожидаемый'
        elif int(w4) == 1:
            w4 = 'догов.'
        if maxn < w[4] and w[4] != 0:
            maxn = w[4]
        if minn > w[4]  and w[4] != 0:
            minn = w[4]
        results += '\nДистрибьютор: ' + w[8] + '\nНазвания: ' + w[0] + '\nПроизводитель: ' + w[9] + '({})'.format(w[10]) + '\nАдрес:' + find_address(w[8]) + '\nЦена сум: ' + str(w4) + '\nТелефон: '+ find_phone(w[8]) + '\n\n➖➖➖➖➖➖➖➖➖➖➖➖\n\n'
        n += 1
        if n == 6:
            results = 'Дата загрузки прайса: ' + d + '\n' + results
            m = bot.send_message(update.message.chat.id, results)
            
            c.execute("INSERT INTO message VALUES ({}, {}) ".format(update.message.chat.id, m.message_id))
            conn.commit()
            results = ''
            n = 0
    if minn != maxn and minn != 0:
        min_and_max = '↗️ Максимальная цена: {} сум.\n↘️ Минимальная цена:  {} сум.'.format(str(maxn), str(minn))
    if n != 0:
        results = 'Дата загрузки прайса: ' + d + '\n' + results
        m = bot.send_message(update.message.chat.id, results)
        print(m)
        c.execute("INSERT INTO message VALUES ({}, {}) ".format(update.message.chat.id, m.message_id))
        conn.commit()
    if minn != maxn and minn != 0:
        m = bot.send_message(update.message.chat.id, min_and_max)
        c.execute("INSERT INTO message VALUES ({}, {}) ".format(update.message.chat.id, m.message_id))
        conn.commit()
# checkng that user has accces to find, no use all 5 chances
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
        c.execute("INSERT INTO access_to_find VALUES ({}, '{}', 500)".format(update.message.chat.id, d))
        conn.commit()
        #update.message.reply_text('Введите название лекарства, а наш бот подскажет Вам возможные варианты:\n\nПример: анальгин\n(Минимум 3 символа)', reply_markup = ReplyKeyboardMarkup(keyboard=[['Назад']], resize_keyboard=True))
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
                #update.message.reply_text('Введите название лекарства, а наш бот подскажет Вам возможные варианты:\n\nПример: анальгин\n(Минимум 3 символа)', reply_markup = ReplyKeyboardMarkup(keyboard=[['Назад']], resize_keyboard=True))
                conn.close()
                return GLOBAL_NAME
        else:
            c.execute("""UPDATE access_to_find SET last_date = '{}' WHERE id={} """.format(current_day, update.message.chat.id))
            c.execute("""UPDATE access_to_find SET chance = 500 WHERE id={} """.format(update.message.chat.id))
            conn.commit()
            #update.message.reply_text('Введите название лекарства, а наш бот подскажет Вам возможные варианты:\n\nПример: анальгин\n(Минимум 3 символа)', reply_markup = ReplyKeyboardMarkup(keyboard=[['Назад']], resize_keyboard=True))
            conn.close()
            return GLOBAL_NAME



def find_address(title):
    try:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM address_and_phone WHERE name LIKE '%{}%' ".format(title.lower()))
        r = c.fetchone()[2]
        if r:
            return r
        else:
            return 'Не указан' 
        conn.close()
    except:
        return 'Не указан'

def find_phone(title):
    try:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM address_and_phone WHERE name LIKE '%{}%' ".format(title.lower()))
        r = c.fetchone()[1]
        if r:
            return r
        else:
            return 'Не указан' 
        conn.close()
    except:
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
        bot = context.bot
        bot.send_chat_action(chat_id=update.message.chat.id, action=ChatAction.TYPING)
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
        bot = context.bot
        doc = bot.get_file(update.message.document.file_id)
        doc.download(update.message.document.file_name)

        p = os.listdir()
        for i in p:
            if i[-3::] == 'xls' or i[-4::] == 'xlsx':
                path = i
                break
        c.execute("SELECT * FROM address_and_phone ")
        for i in c.fetchall():
            c.execute("DELETE FROM address_and_phone ")
        conn.commit()
        df = pd.read_excel('{}'.format(path), sheet_name=1)
        for i in df.values.tolist():
        
            try:

                c.execute("INSERT INTO address_and_phone VALUES ('{}','{}','{}') ".format(i[1].lower(), i[2], i[3]))

            except:
                fnwow = 0
        conn.commit()
        conn.close()


        if issuperadmin(update.message.chat.id):
            update.message.reply_text("главный админ панель бота", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
        else:
            update.message.reply_text("админ панель бота", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас🧾'], ['Наши партнеры🤝'], ['Наш сайт']], resize_keyboard=True))
        return SUPERADMIN

def cancel(update, context):
    bot = context.bot
    c = update.callback_query 
    if update.callback_query.data == 'next':
        c.edit_message_text('Нажмите /start для перезапустить бот')
        return ConversationHandler.END

