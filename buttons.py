import bot
import sqlite3
from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from conversationList import GLOBAL_NAME, SELECT_DRUGS, SUPERADMIN, UPDATE_EXCEL, START, EDIT_ABOUT_US, UPDATE_ABOUT_US, EDIT_OUR_PARTNERS, UPDATE_OUR_PARTNERS, EDIT_OUR_SITE
from conversationList import UPDATE_OUR_SITE, CREATE_ADMIN, ADD_REMOVE_ADMIN, DELETE_ADMIN, WRITE_NAME, SEND_PHONE, SETTINGS, UPDATE_NAME, UPDATE_PHONE
from functions import change_sort_type
def find_drug(update, context):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM access_to_find WHERE id={} ".format(update.message.chat.id))
    fetchone = c.fetchone()
    f = update.message.date
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
                
                update.message.reply_text('Лимит на ежедневный поиск 5 раз\nВы использовали все это')
                
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
    
    update.message.reply_text('Настройки\nВы можете изменить свое имя и номер телефона в меню «Профиль».\nА также настройки сортировки данных.', reply_markup=ReplyKeyboardMarkup(keyboard=[['Профиль'], ['Сортировки'], ['Назад⬅️']], resize_keyboard=True))
    return SETTINGS


def setting_menus(update, context):
    text = update.message.text
    print(text)
    bot = context.bot
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    if text == 'Профиль':
        c.execute("SELECT * FROM users WHERE id={}".format(update.message.chat.id))
        obj = c.fetchone()
        update.message.reply_text('Имя: {} \n Номер телефон: {}  '.format(obj[1], obj[2]), reply_markup=ReplyKeyboardMarkup(keyboard=[['изменить имя'], ['изменить номер телефона'], ['назад⏪']], resize_keyboard=True))
    if text == 'изменить имя':
        update.message.reply_text('напишите новое имя:', reply_markup=ReplyKeyboardRemove(remove_keyboard = True))
        return UPDATE_NAME
    if text == 'изменить номер телефона':
        update.message.reply_text('напишите новый номер телефона', reply_markup=ReplyKeyboardRemove(remove_keyboard = True))
        return UPDATE_PHONE
    if text == 'назад⏪':
        update.message.reply_text('Настройки\nВы можете изменить свое имя и номер телефона в меню «Профиль».\nА также настройки сортировки данных.', reply_markup=ReplyKeyboardMarkup(keyboard=[['Профиль'], ['Сортировки'], ['Назад⬅️']], resize_keyboard=True))
        return SETTINGS
    if text == 'Назад⬅️':
        update.message.reply_text("Вас приветствует бот по поиску лекарств о компании название компании", reply_markup=ReplyKeyboardMarkup(keyboard=[['Поиск лекарств🔎'], ['О нас🔎'], ['Наши партнеры🤝'], ['Наш сайт'], ['Настройки⚙️']], resize_keyboard=True))
        return ConversationHandler.END
    if text == 'Сортировки':   #sort
        c.execute("SELECT * FROM sort WHERE id={} ".format(update.message.chat.id))
        mrk = ReplyKeyboardMarkup(keyboard=[['вернуться к настройкам']], resize_keyboard=True)
        update.message.reply_text('настройка сортировки', reply_markup=mrk)
        
        if not c.fetchall():
            print(2)
            c.execute("INSERT INTO sort VALUES ({}, 'цене', 'возрастание', 'возрастание')".format(update.message.chat.id))
            i_by_price = InlineKeyboardButton(text='сортировать по цене', callback_data='by_price')
            i_by_procent = InlineKeyboardButton(text='сортировать по процентам', callback_data='by_procent')

            update.message.reply_text('Ваша сортировка по: цене \nпо:   возрастание', reply_markup=InlineKeyboardMarkup([[i_by_price], [i_by_procent]]))
    
        else:
            
            c.execute("SELECT * FROM sort WHERE id={} ".format(update.message.chat.id))
            obj = c.fetchall()[0]
            if obj[1] == 'цене':
                price_or_procent = obj[2]
                
            elif obj[1] == 'процентам':
                price_or_procent = obj[3]

            i_by_price = InlineKeyboardButton(text='сортировать по цене', callback_data='by_price')
            i_by_procent = InlineKeyboardButton(text='сортировать по процентам', callback_data='by_procent')
            update.message.reply_text('Ваша сортировка по: {} \nпо:   {}'.format(obj[1], price_or_procent), reply_markup=InlineKeyboardMarkup([[i_by_price], [i_by_procent]]))
    
    
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
    c.execute("SELECT * FROM users WHERE id={}".format(update.message.chat.id))
    obj = c.fetchone()
    update.message.reply_text('Имя: {} \n Номер телефон: {}  '.format(obj[1], obj[2]), reply_markup=ReplyKeyboardMarkup(keyboard=[['изменить имя'], ['изменить номер телефона'], ['назад⏪']], resize_keyboard=True))
    
    conn.close()
    
    return SETTINGS


def update_phone(update, context):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""UPDATE users SET phone_number = '{}' WHERE id={} """.format(update.message.text, update.message.chat.id))
    conn.commit()
    c.execute("SELECT * FROM users WHERE id={}".format(update.message.chat.id))
    obj = c.fetchone()
    update.message.reply_text('Имя: {} \n Номер телефон: {}  '.format(obj[1], obj[2]), reply_markup=ReplyKeyboardMarkup(keyboard=[['изменить имя'], ['изменить номер телефона'], ['назад⏪']], resize_keyboard=True))
    
    conn.close()
    
   
    return SETTINGS


