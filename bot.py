from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ChatAction
import xlrd
import os
from conversationList import GLOBAL_NAME, SELECT_DRUGS, SUPERADMIN, UPDATE_EXCEL, START, EDIT_ABOUT_US, UPDATE_ABOUT_US
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
    print(update.message.date)
    admins = []
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM admins ")
    for i in c.fetchall():

        admins.append(i[0]) 
    
    conn.commit()
    conn.close()   
    if update.message.chat.id == superadmin:
        update.message.reply_text("hi super", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
        
        return SUPERADMIN
    elif update.message.chat.id in admins:
        update.message.reply_text("hi admin", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт']], resize_keyboard=True))
        return SUPERADMIN
    else:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM sort WHERE id={} ".format(update.message.chat.id))
        if not c.fetchall():
            c.execute("INSERT INTO sort VALUES ({}, 'цене', 'возрастание', 'возрастание')".format(update.message.chat.id))

        update.message.reply_text("hi", reply_markup=ReplyKeyboardMarkup(keyboard=[['Поиск лекарств'], ['О нас '], ['Наши партнеры'], ['Наш сайт'], ['Настройки']], resize_keyboard=True))
    
    
def global_name(update, context):
    bot = context.bot
    text = update.message.text 
    if text == 'Назад':
        update.message.reply_text("hi", reply_markup=ReplyKeyboardMarkup(keyboard=[['Поиск лекарств'], ['О нас '], ['Наши партнеры'], ['Наш сайт'], ['Настройки']], resize_keyboard=True))
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
            mrk = [[KeyboardButton(text='назад')]]
            update.message.reply_text('no drugs, reenter', reply_markup=ReplyKeyboardMarkup(mrk, resize_keyboard=True, one_time_keyboard=True))
            return GLOBAL_NAME
        else:
            for i in r:
                w = worksheet.row_values(i)
                if not w[0] in texts:
                    texts.append(w[0])
                    items.append([KeyboardButton(text=w[0])])
            items.append([KeyboardButton(text='cancel'), KeyboardButton(text='Главная')])
            update.message.reply_text('select drug name', reply_markup=ReplyKeyboardMarkup(items, resize_keyboard=True, one_time_keyboard=True))
            return SELECT_DRUGS
    

def select_drugs(update, context):
    bot = context.bot
    name = update.message.text
    if name == 'Главная':
        update.message.reply_text("hi", reply_markup=ReplyKeyboardMarkup(keyboard=[['Поиск лекарств'], ['О нас '], ['Наши партнеры'], ['Наш сайт'], ['Настройки']], resize_keyboard=True))
        return ConversationHandler.END
    if name == 'Назад':
        update.message.reply_text('write global name:', reply_markup = ReplyKeyboardMarkup(keyboard=[['Назад']], resize_keyboard=True))
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
        for w in all:
            if w[4] == 0:
                w[4] = 'ожидаемый'
            results += '\nНазвания: ' + w[0] + '\nПроизводитель: ' + w[9] + '({})'.format(w[10]) + '\nАдрес:' + find_address(w[8]) + '\nЦена сум: ' + str(w[4]) + '\nЦена в долларах США: ' + str(w[5]) + '\nЦена в ЕВРО: ' + str(w[6]) + '\nТелефон: '+ find_phone(w[8]) + '\n\n\n\n\n'
        
        results = 'дата загрузки прайса: ' + d + results
        bot.send_message(update.message.chat.id, results)
        update.message.reply_text("hi", reply_markup=ReplyKeyboardMarkup(keyboard=[['Поиск лекарств'], ['О нас '], ['Наши партнеры'], ['Наш сайт'], ['Настройки']], resize_keyboard=True))
        return ConversationHandler.END        
    

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
        return ''

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
        return ''



def doc(update, context):
    print('d')
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
            update.message.reply_text("hi super", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
        else:
            update.message.reply_text("hi admin", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт']], resize_keyboard=True))
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
        update.message.reply_text("hi super", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас '], ['Наши партнеры'], ['Наш сайт'], ['Добавить админ']], resize_keyboard=True))

        return SUPERADMIN

def cancel(update, context):
    print('done')

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, update.error)

def find(update, context, content_types=["text", "sticker", "pinned_message", "photo", "audio"]):
    print("kajsoia")
