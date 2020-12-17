import bot
import sqlite3
from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from conversationList import GLOBAL_NAME, SELECT_DRUGS, SUPERADMIN, UPDATE_EXCEL, START, EDIT_ABOUT_US, UPDATE_ABOUT_US, EDIT_OUR_PARTNERS, UPDATE_OUR_PARTNERS, EDIT_OUR_SITE
from conversationList import UPDATE_OUR_SITE, CREATE_ADMIN, ADD_REMOVE_ADMIN, DELETE_ADMIN, WRITE_NAME, SEND_PHONE, SETTINGS, UPDATE_NAME, UPDATE_PHONE
from functions import change_sort_type
def find_drug(update, context):
    update.message.reply_text('write global name:', reply_markup = ReplyKeyboardMarkup(keyboard=[['Назад']], resize_keyboard=True))
    return GLOBAL_NAME

def about_us(update, context):
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM menus")
    update.message.reply_text(c.fetchall()[0][0])
    conn.commit()
    conn.close()

def our_partners(update, message):
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM menus")
    update.message.reply_text(c.fetchall()[0][1])
    conn.commit()
    conn.close()


def our_site(update, context):
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM menus")
    update.message.reply_text(c.fetchall()[0][2])
    conn.commit()
    conn.close()

# settings
def settings(update, context):
    
    update.message.reply_text('settings', reply_markup=ReplyKeyboardMarkup(keyboard=[['profile'], ['sort'], ['cancel1']], resize_keyboard=True))
    return SETTINGS


def setting_menus(update, context):
    text = update.message.text
    print(text)
    bot = context.bot
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    if text == 'profile':
        c.execute("SELECT * FROM users WHERE id={}".format(update.message.chat.id))
        obj = c.fetchone()
        update.message.reply_text('name: {} \n phone: {}  '.format(obj[1], obj[2]), reply_markup=ReplyKeyboardMarkup(keyboard=[['name'], ['phone'], ['cancel2']], resize_keyboard=True))
    if text == 'name':
        update.message.reply_text('write name:')
        return UPDATE_NAME
    if text == 'phone':
        update.message.reply_text('write phone:')
        return UPDATE_PHONE
    if text == 'cancel2':
        update.message.reply_text('settings', reply_markup=ReplyKeyboardMarkup(keyboard=[['profile'], ['sort'], ['cancel1']], resize_keyboard=True))
        return SETTINGS
    if text == 'cancel1':
        update.message.reply_text("hi", reply_markup=ReplyKeyboardMarkup(keyboard=[['Поиск лекарств'], ['О нас '], ['Наши партнеры'], ['Наш сайт'], ['Настройки']], resize_keyboard=True))
        return ConversationHandler.END
    if text == 'sort':   #sort
        c.execute("SELECT * FROM sort WHERE id={} ".format(update.message.chat.id))
        mrk = ReplyKeyboardMarkup(keyboard=[['вернуться к настройкам']], resize_keyboard=True)
        update.message.reply_text('sort settings', reply_markup=mrk)
        
        if not c.fetchall():
            print(2)
            c.execute("INSERT INTO sort VALUES ({}, 'цене', 'возрастание', 'возрастание')".format(update.message.chat.id))
            i_by_price = InlineKeyboardButton(text='сортировать по цене', callback_data='by_price')
            i_by_procent = InlineKeyboardButton(text='сортировать по процентам', callback_data='by_procent')

            update.message.reply_text('Сортировка по: цене \nпо:   возрастание', reply_markup=InlineKeyboardMarkup([[i_by_price], [i_by_procent]]))
    
        else:
            
            c.execute("SELECT * FROM sort WHERE id={} ".format(update.message.chat.id))
            obj = c.fetchall()[0]
            if obj[1] == 'цене':
                price_or_procent = obj[2]
                
            elif obj[1] == 'процентам':
                price_or_procent = obj[3]

            i_by_price = InlineKeyboardButton(text='сортировать по цене', callback_data='by_price')
            i_by_procent = InlineKeyboardButton(text='сортировать по процентам', callback_data='by_procent')
            update.message.reply_text('Сортировка по: {} \nпо:   {}'.format(obj[1], price_or_procent), reply_markup=InlineKeyboardMarkup([[i_by_price], [i_by_procent]]))
    
    
        conn.commit()
        conn.close()    
        return ConversationHandler.END
    conn.commit()
    conn.close()



def update_name(update, context):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""UPDATE users SET name = '{}' WHERE id={} """.format(update.message.text, update.message.chat.id))

    conn.commit()
    conn.close()
    
    update.message.reply_text('name is changes')
    return SETTINGS


def update_phone(update, context):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""UPDATE users SET phone_number = '{}' WHERE id={} """.format(update.message.text, update.message.chat.id))

    conn.commit()
    conn.close()
    
    update.message.reply_text('phone is changed')
    return SETTINGS


