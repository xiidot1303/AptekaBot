import bot
from bot import issuperadmin
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from conversationList import GLOBAL_NAME, SELECT_DRUGS, SUPERADMIN, UPDATE_EXCEL, START, EDIT_ABOUT_US, UPDATE_ABOUT_US, START, EDIT_OUR_PARTNERS, UPDATE_OUR_PARTNERS, UPDATE_OUR_SITE
from conversationList import EDIT_OUR_SITE, ADD_REMOVE_ADMIN
from conversationList import CREATE_ADMIN, DELETE_ADMIN
def superadmin(update, context):
    text = update.message.text
    if text == 'Обновить Excel':
        mrk = ReplyKeyboardMarkup(keyboard=[['назад']])
        update.message.reply_text("Send new file", reply_markup=mrk)
        return UPDATE_EXCEL
    elif text == 'О нас':
        
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM menus")
        i_edit = KeyboardButton(text='Изменить')
        i_cancel = KeyboardButton(text='Назад')
        update.message.reply_text(c.fetchall()[0][0], reply_markup=ReplyKeyboardMarkup([[i_edit, i_cancel]], resize_keyboard=True, one_time_keyboard=True))
        conn.commit()
        conn.close()
        
        return EDIT_ABOUT_US
    elif text == 'Наши партнеры':
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM menus")
        i_edit = KeyboardButton(text='Изменить')
        i_cancel = KeyboardButton(text='Назад')
        update.message.reply_text(c.fetchall()[0][1], reply_markup=ReplyKeyboardMarkup([[i_edit, i_cancel]], resize_keyboard=True, one_time_keyboard=True))
        conn.commit()
        conn.close()
        return EDIT_OUR_PARTNERS
    elif text == 'Наш сайт':
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM menus")
        i_edit = KeyboardButton(text='Изменить')
        i_cancel = KeyboardButton(text='Назад')
        update.message.reply_text(c.fetchall()[0][2], reply_markup=ReplyKeyboardMarkup([[i_edit, i_cancel]], resize_keyboard=True, one_time_keyboard=True))
        conn.commit()
        conn.close()
        return EDIT_OUR_SITE
    elif text == 'Админы':
        if issuperadmin(update.message.chat.id):
            conn = sqlite3.connect('data.db')
            c = conn.cursor()

            c.execute("SELECT * FROM admins ")
            admin_list = ''
            n = 1
            for i in c.fetchall():
                admin_list += str(n) + '.'
                for x in i:
                    
                    admin_list += '       ' + str(x)
                admin_list += '\n'
            
                n += 1
            
            update.message.reply_text(admin_list, reply_markup=ReplyKeyboardMarkup(keyboard=[['add admin', 'remove', 'Назад']], resize_keyboard=True))

            conn.commit()
            conn.close()
            return ADD_REMOVE_ADMIN
def edit_our_site(update, context):
    text = update.message.text
    if text == 'Изменить':
        mrk = ReplyKeyboardRemove(remove_keyboard=True)
        update.message.reply_text('Send new our site', reply_markup=mrk)
        return UPDATE_OUR_SITE
    elif text == 'Назад':
    
        if issuperadmin(update.message.chat.id):
            update.message.reply_text("hi super", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
        else:
            update.message.reply_text("hi admin", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт']], resize_keyboard=True))
        return SUPERADMIN    
def update_our_site(update, context):
    text = update.message.chat.id
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()    
    c.execute("""UPDATE menus SET our_site = '{}' """.format(update.message.text))

    conn.commit()
    conn.close()
    if issuperadmin(update.message.chat.id):
        update.message.reply_text("hi super", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
    else:
        update.message.reply_text("hi admin", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт']], resize_keyboard=True))
    return SUPERADMIN    


def edit_our_partners(update, context):
    text = update.message.text
    if text == 'Изменить':
        
        mrk = ReplyKeyboardRemove(remove_keyboard=True)
        update.message.reply_text('Send new our partners ', reply_markup=mrk)
        return UPDATE_OUR_PARTNERS
    elif text == 'Назад':
        
        if issuperadmin(update.message.chat.id):
            update.message.reply_text("hi super", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
        else:
            update.message.reply_text("hi admin", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт']], resize_keyboard=True))
        return SUPERADMIN
def update_our_partners(update, context):    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    c.execute("""UPDATE menus SET our_partners = '{}' """.format(update.message.text))

    conn.commit()
    conn.close()
    if issuperadmin(update.message.chat.id):
        update.message.reply_text("hi super", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
    else:
        update.message.reply_text("hi admin", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт']], resize_keyboard=True))
    return SUPERADMIN    



def edit_about_us(update, context):
    text = update.message.text
    if text == 'Изменить':
        
        mrk = ReplyKeyboardRemove(remove_keyboard=True)
        update.message.reply_text('Send new about us ', reply_markup=mrk)
        return UPDATE_ABOUT_US
    elif text == 'Назад':
    
        if issuperadmin(update.message.chat.id):
            update.message.reply_text("hi super", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
        else:
            update.message.reply_text("hi admin", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт']], resize_keyboard=True))
        return SUPERADMIN
def update_about_us(update, context):
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    c.execute("""UPDATE menus SET about_us = '{}' """.format(update.message.text))
    
    
    conn.commit()
    conn.close()
    if issuperadmin(update.message.chat.id):
        update.message.reply_text("hi super", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
    else:
        update.message.reply_text("hi admin", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт']], resize_keyboard=True))
    return SUPERADMIN



def add_remove_admin(update, context):
    text = update.message.text
    if text == 'add admin':
        update.message.reply_text('send forwrded message', reply_markup=ReplyKeyboardRemove(remove_keyboard = True))
        return CREATE_ADMIN
    if text == 'remove':
        update.message.reply_text('pls. enter id admin:', reply_markup=ReplyKeyboardRemove(remove_keyboard = True))
        return DELETE_ADMIN
    elif text == 'Назад':
    
        if issuperadmin(update.message.chat.id):
            update.message.reply_text("hi super", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
        else:
            update.message.reply_text("hi admin", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт']], resize_keyboard=True))
        return SUPERADMIN


def create_admin(update, context):
    print(update.message.forward_from)
    if update.message.forward_from == None:
        update.message.reply_text('such user dont permitted forward theri messages')
        return CREATE_ADMIN
    
    else:
        
        obj = update.message.forward_from
        print(obj)
        if not obj.username == None:
            username = '@'+obj.username
        else:
            username = ''
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("INSERT INTO admins VALUES ({}, '{}', '{}')".format(int(obj.id), obj.first_name, username))
        
        conn.commit()
        conn.close()
        update.message.reply_text("hi super", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
        return SUPERADMIN




def delete_admin(update, context):
    bot = context.bot
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM admins WHERE id={} ".format(int(update.message.text)))
        
        conn.commit()
        conn.close()
        update.message.reply_text("hi super", reply_markup=ReplyKeyboardMarkup(keyboard=[['Обновить Excel'], ['О нас'], ['Наши партнеры'], ['Наш сайт'], ['Админы']], resize_keyboard=True))
        return SUPERADMIN
    except:
        update.message.reply_text('error, write correct')
        
        conn.commit()
        conn.close()
        return DELETE_ADMIN


