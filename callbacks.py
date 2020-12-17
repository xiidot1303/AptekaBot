import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from conversationList import GLOBAL_NAME, SELECT_DRUGS, SUPERADMIN, UPDATE_EXCEL, START, EDIT_ABOUT_US, UPDATE_ABOUT_US, EDIT_OUR_PARTNERS, UPDATE_OUR_PARTNERS, EDIT_OUR_SITE
from conversationList import UPDATE_OUR_SITE, CREATE_ADMIN, ADD_REMOVE_ADMIN, REMOVE_ADMIN, DELETE_ADMIN, WRITE_NAME, SEND_PHONE
from functions import change_sort_type
from telegram.ext import ConversationHandler
def callback(update, context):

    bot = context.bot
    cq = update.callback_query
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    #price
    if cq.data == 'by_price':
        i_wane = InlineKeyboardButton(text='убывание', callback_data='price_to_убывание')
        i_grow = InlineKeyboardButton(text='возрастание', callback_data='price_to_возрастание')
        i_cancel = InlineKeyboardButton(text='Назад', callback_data='sort')
        cq.edit_message_text('sort price po', reply_markup=InlineKeyboardMarkup([[i_grow], [i_wane], [i_cancel]]))

    if cq.data == 'by_procent':
        i_wane = InlineKeyboardButton(text='убывание', callback_data='procent_to_убывание')
        i_grow = InlineKeyboardButton(text='возрастание', callback_data='procent_to_возрастание')
        i_cancel = InlineKeyboardButton(text='Назад', callback_data='sort')
        cq.edit_message_text('sort price po', reply_markup=InlineKeyboardMarkup([[i_grow], [i_wane], [i_cancel]]))


    if cq.data == 'price_to_убывание':
        
        c.execute("""UPDATE sort SET price = 'убывание' WHERE id={} """.format(cq.message.chat.id))
        c.execute("""UPDATE sort SET sort_by = 'цене' WHERE id={} """.format(cq.message.chat.id))
        conn.commit()
        c.execute("SELECT * FROM sort WHERE id={} ".format(cq.message.chat.id))
        obj = c.fetchall()[0]
        if obj[1] == 'цене':
            price_or_procent = obj[2]
            
        elif obj[1] == 'процентам':
            price_or_procent = obj[3]
        
        i_by_price = InlineKeyboardButton(text='сортировать по цене', callback_data='by_price')
        i_by_procent = InlineKeyboardButton(text='сортировать по процентам', callback_data='by_procent')
        cq.edit_message_text('Сортировка по: {} \nпо:   {}'.format(obj[1], price_or_procent), reply_markup=InlineKeyboardMarkup([[i_by_price], [i_by_procent]]))
    if cq.data == 'price_to_возрастание':
        
        c.execute("""UPDATE sort SET price = 'возрастание' WHERE id={} """.format(cq.message.chat.id))
        c.execute("""UPDATE sort SET sort_by = 'цене' WHERE id={} """.format(cq.message.chat.id))
        conn.commit()
        c.execute("SELECT * FROM sort WHERE id={} ".format(cq.message.chat.id))
        obj = c.fetchall()[0]
        if obj[1] == 'цене':
            price_or_procent = obj[2]
            
        elif obj[1] == 'процентам':
            price_or_procent = obj[3]
        
        i_by_price = InlineKeyboardButton(text='сортировать по цене', callback_data='by_price')
        i_by_procent = InlineKeyboardButton(text='сортировать по процентам', callback_data='by_procent')
        cq.edit_message_text('Сортировка по: {} \nпо:   {}'.format(obj[1], price_or_procent), reply_markup=InlineKeyboardMarkup([[i_by_price], [i_by_procent]]))

    if cq.data == 'procent_to_убывание':

        c.execute("""UPDATE sort SET procent = 'убывание' WHERE id={} """.format(cq.message.chat.id))
        c.execute("""UPDATE sort SET sort_by = 'процентам' WHERE id={} """.format(cq.message.chat.id))
        conn.commit()
        c.execute("SELECT * FROM sort WHERE id={} ".format(cq.message.chat.id))
        obj = c.fetchall()[0]
        if obj[1] == 'цене':
            price_or_procent = obj[2]
            
        elif obj[1] == 'процентам':
            price_or_procent = obj[3]
        
        i_by_price = InlineKeyboardButton(text='сортировать по цене', callback_data='by_price')
        i_by_procent = InlineKeyboardButton(text='сортировать по процентам', callback_data='by_procent')
        cq.edit_message_text('Сортировка по: {} \nпо:   {}'.format(obj[1], price_or_procent), reply_markup=InlineKeyboardMarkup([[i_by_price], [i_by_procent]]))
    
    if cq.data == 'procent_to_возрастание':
        
        c.execute("""UPDATE sort SET procent = 'возрастание' WHERE id={} """.format(cq.message.chat.id))
        c.execute("""UPDATE sort SET sort_by = 'процентам' WHERE id={} """.format(cq.message.chat.id))
        conn.commit()
        c.execute("SELECT * FROM sort WHERE id={} ".format(cq.message.chat.id))
        obj = c.fetchall()[0]
        if obj[1] == 'цене':
            price_or_procent = obj[2]
            
        elif obj[1] == 'процентам':
            price_or_procent = obj[3]
        
        i_by_price = InlineKeyboardButton(text='сортировать по цене', callback_data='by_price')
        i_by_procent = InlineKeyboardButton(text='сортировать по процентам', callback_data='by_procent')
        cq.edit_message_text('Сортировка по: {} \nпо:   {}'.format(obj[1], price_or_procent), reply_markup=InlineKeyboardMarkup([[i_by_price], [i_by_procent]]))
    if cq.data == 'sort':
        c.execute("SELECT * FROM sort WHERE id={} ".format(cq.message.chat.id))
        obj = c.fetchall()[0]
        if obj[1] == 'цене':
            price_or_procent = obj[2]
            
        elif obj[1] == 'процентам':
            price_or_procent = obj[3]
        
        i_by_price = InlineKeyboardButton(text='сортировать по цене', callback_data='by_price')
        i_by_procent = InlineKeyboardButton(text='сортировать по процентам', callback_data='by_procent')
        cq.edit_message_text('Сортировка по: {} \nпо:   {}'.format(obj[1], price_or_procent), reply_markup=InlineKeyboardMarkup([[i_by_price], [i_by_procent]]))
    if cq.data == 'settings':        
        bot.send_message(cq.message.chat.id, 'settings', reply_markup=ReplyKeyboardMarkup(keyboard=[['profile'], ['sort'], ['cancel1']], resize_keyboard=True))
        return ConversationHandler.states.SETTINGS
    if cq.data == 'sort_by_цене':
        print('by price')
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
        print('by procent')
        c.execute("""UPDATE sort SET sort_by = 'процентам' WHERE id={} """.format(cq.message.chat.id))
        conn.commit()
        c.execute("SELECT * FROM sort WHERE id={} ".format(cq.message.chat.id))
        obj = c.fetchall()[0]
        
        if obj[1] == 'цене':
            price_or_procent = obj[2]
        elif obj[1] == 'процентам':
            price_or_procent = obj[3]
        print(obj[3])
        i_change_price_or_procent = InlineKeyboardButton(text='по {}'.format(change_sort_type(price_or_procent)), callback_data='procent_to_{}'.format(change_sort_type(price_or_procent)))
        i_change_sort = InlineKeyboardButton(text='сортировать по {}'.format(change_sort_type(obj[1])), callback_data='sort_by_{}'.format(change_sort_type(obj[1])))
        
        cq.edit_message_text('Сортировка по: {} \nпо:   {}'.format(obj[1], price_or_procent), reply_markup=InlineKeyboardMarkup([[i_change_price_or_procent],[i_change_sort]]))
