import bot
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from conversationList import GLOBAL_NAME, SELECT_DRUGS, SUPERADMIN, UPDATE_EXCEL, START, EDIT_ABOUT_US, UPDATE_ABOUT_US
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

def settings(update, context):
    update.message.reply_text('settings')

