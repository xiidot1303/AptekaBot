import bot
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from conversationList import GLOBAL_NAME, SELECT_DRUGS, SUPERADMIN, UPDATE_EXCEL, START, EDIT_ABOUT_US, UPDATE_ABOUT_US
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
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sort WHERE id={} ".format(update.message.chat.id))
    
    if not c.fetchall():

        c.execute("INSERT INTO sort VALUES ({}, 'цене', 'возрастание', 'возрастание')".format(update.message.chat.id))

        i_change_sort = InlineKeyboardButton(text='сортировать по процентам', callback_data='sort_by_процентам')
        i_change_price = InlineKeyboardButton(text='по {}'.format(change_sort_type('возрастание')), callback_data='price_to_убывание')
        update.message.reply_text('Сортировка по: цене \nпо:   возрастание', reply_markup=InlineKeyboardMarkup([[i_change_price], [i_change_sort]]))

    else:
        
        c.execute("SELECT * FROM sort WHERE id={} ".format(update.message.chat.id))
        obj = c.fetchall()[0]
        if obj[1] == 'цене':
            price_or_procent = obj[2]
            i_change_price_or_procent = InlineKeyboardButton(text='по {}'.format(change_sort_type(price_or_procent)), callback_data='price_to_{}'.format(change_sort_type(price_or_procent)))
        elif obj[1] == 'процентам':
            price_or_procent = obj[3]
            i_change_price_or_procent = InlineKeyboardButton(text='по {}'.format(change_sort_type(price_or_procent)), callback_data='procent_to_{}'.format(change_sort_type(price_or_procent)))
        
        
        
        i_change_sort = InlineKeyboardButton(text='сортировать по {}'.format(change_sort_type(obj[1])), callback_data='sort_by_{}'.format(change_sort_type(obj[1])))
        
        update.message.reply_text('Сортировка по: {} \nпо:   {}'.format(obj[1], price_or_procent), reply_markup=InlineKeyboardMarkup([[i_change_price_or_procent],[i_change_sort]]))

    conn.commit()
    conn.close()


def callback(update, context):
    bot = context.bot
    cq = update.callback_query
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    #price
    if cq.data == 'price_to_убывание':

        c.execute("""UPDATE sort SET price = 'убывание' WHERE id={} """.format(cq.message.chat.id))
        conn.commit()
        c.execute("SELECT * FROM sort WHERE id={} ".format(cq.message.chat.id))
        obj = c.fetchall()[0]
        if obj[1] == 'цене':
            price_or_procent = obj[2]
        elif obj[1] == 'процентам':
            price_or_procent = obj[3]
    
        i_change_price_or_procent = InlineKeyboardButton(text='по {}'.format(change_sort_type(price_or_procent)), callback_data='price_to_{}'.format(change_sort_type(price_or_procent)))
        i_change_sort = InlineKeyboardButton(text='сортировать по {}'.format(change_sort_type(obj[1])), callback_data='sort_by_{}'.format(change_sort_type(obj[1])))
        
        cq.edit_message_text('Сортировка по: {} \nпо:   {}'.format(obj[1], price_or_procent), reply_markup=InlineKeyboardMarkup([[i_change_price_or_procent],[i_change_sort]]))
    
    if cq.data == 'price_to_возрастание':
        
        c.execute("""UPDATE sort SET price = 'возрастание' WHERE id={} """.format(cq.message.chat.id))
        conn.commit()
        c.execute("SELECT * FROM sort WHERE id={} ".format(cq.message.chat.id))
        obj = c.fetchall()[0]
        if obj[1] == 'цене':
            price_or_procent = obj[2]
        elif obj[1] == 'процентам':
            price_or_procent = obj[3]
    
        i_change_price_or_procent = InlineKeyboardButton(text='по {}'.format(change_sort_type(price_or_procent)), callback_data='price_to_{}'.format(change_sort_type(price_or_procent)))
        i_change_sort = InlineKeyboardButton(text='сортировать по {}'.format(change_sort_type(obj[1])), callback_data='sort_by_{}'.format(change_sort_type(obj[1])))
        
        cq.edit_message_text('Сортировка по: {} \nпо:   {}'.format(obj[1], price_or_procent), reply_markup=InlineKeyboardMarkup([[i_change_price_or_procent],[i_change_sort]]))
        #procent
    
    if cq.data == 'procent_to_убывание':

        c.execute("""UPDATE sort SET procent = 'убывание' WHERE id={} """.format(cq.message.chat.id))
        conn.commit()
        c.execute("SELECT * FROM sort WHERE id={} ".format(cq.message.chat.id))
        obj = c.fetchall()[0]
        if obj[1] == 'цене':
            price_or_procent = obj[2]
        elif obj[1] == 'процентам':
            price_or_procent = obj[3]
    
        i_change_price_or_procent = InlineKeyboardButton(text='по {}'.format(change_sort_type(price_or_procent)), callback_data='procent_to_{}'.format(change_sort_type(price_or_procent)))
        i_change_sort = InlineKeyboardButton(text='сортировать по {}'.format(change_sort_type(obj[1])), callback_data='sort_by_{}'.format(change_sort_type(obj[1])))
        
        cq.edit_message_text('Сортировка по: {} \nпо:   {}'.format(obj[1], price_or_procent), reply_markup=InlineKeyboardMarkup([[i_change_price_or_procent],[i_change_sort]]))
    
    if cq.data == 'procent_to_возрастание':
        
        c.execute("""UPDATE sort SET procent = 'возрастание' WHERE id={} """.format(cq.message.chat.id))
        conn.commit()
        c.execute("SELECT * FROM sort WHERE id={} ".format(cq.message.chat.id))
        obj = c.fetchall()[0]
        if obj[1] == 'цене':
            price_or_procent = obj[2]
        elif obj[1] == 'процентам':
            price_or_procent = obj[3]
    
        i_change_price_or_procent = InlineKeyboardButton(text='по {}'.format(change_sort_type(price_or_procent)), callback_data='procent_to_{}'.format(change_sort_type(price_or_procent)))
        i_change_sort = InlineKeyboardButton(text='сортировать по {}'.format(change_sort_type(obj[1])), callback_data='sort_by_{}'.format(change_sort_type(obj[1])))
        
        cq.edit_message_text('Сортировка по: {} \nпо:   {}'.format(obj[1], price_or_procent), reply_markup=InlineKeyboardMarkup([[i_change_price_or_procent],[i_change_sort]]))
    if cq.data == 'sort_by_цене':
        
        c.execute("""UPDATE sort SET sort_by = 'цене' WHERE id={} """.format(cq.message.chat.id))
        conn.commit()
        c.execute("SELECT * FROM sort WHERE id={} ".format(cq.message.chat.id))
        obj = c.fetchall()[0]
        if obj[1] == 'цене':
            price_or_procent = obj[2]
        elif obj[1] == 'процентам':
            price_or_procent = obj[3]
    
        i_change_price_or_procent = InlineKeyboardButton(text='по {}'.format(change_sort_type(price_or_procent)), callback_data='price_to_{}'.format(change_sort_type(price_or_procent)))
        i_change_sort = InlineKeyboardButton(text='сортировать по {}'.format(change_sort_type(obj[1])), callback_data='sort_by_{}'.format(change_sort_type(obj[1])))
        
        cq.edit_message_text('Сортировка по: {} \nпо:   {}'.format(obj[1], price_or_procent), reply_markup=InlineKeyboardMarkup([[i_change_price_or_procent],[i_change_sort]]))
    if cq.data == 'sort_by_процентам':
        
        c.execute("""UPDATE sort SET sort_by = 'процентам' WHERE id={} """.format(cq.message.chat.id))
        conn.commit()
        c.execute("SELECT * FROM sort WHERE id={} ".format(cq.message.chat.id))
        obj = c.fetchall()[0]
        
        if obj[1] == 'цене':
            price_or_procent = obj[2]
        elif obj[1] == 'процентам':
            price_or_procent = obj[3]
        
        i_change_price_or_procent = InlineKeyboardButton(text='по {}'.format(change_sort_type(price_or_procent)), callback_data='procent_to_{}'.format(change_sort_type(price_or_procent)))
        i_change_sort = InlineKeyboardButton(text='сортировать по {}'.format(change_sort_type(obj[1])), callback_data='sort_by_{}'.format(change_sort_type(obj[1])))
        
        cq.edit_message_text('Сортировка по: {} \nпо:   {}'.format(obj[1], price_or_procent), reply_markup=InlineKeyboardMarkup([[i_change_price_or_procent],[i_change_sort]]))
        