from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from bot import start, global_name, select_drugs, doc, cancel, update_excel, forward, write_name, send_phone
from buttons import find_drug, about_us, our_partners, our_site, settings, setting_menus, update_name, update_phone
from admin import superadmin, edit_about_us, update_about_us, edit_our_partners, update_our_partners, edit_our_site, update_our_site, create_admin, add_remove_admin, delete_admin
from conversationList import GLOBAL_NAME, SELECT_DRUGS, SUPERADMIN, UPDATE_EXCEL, START, EDIT_ABOUT_US, UPDATE_ABOUT_US, EDIT_OUR_PARTNERS, UPDATE_OUR_PARTNERS, EDIT_OUR_SITE
from conversationList import UPDATE_OUR_SITE, CREATE_ADMIN, ADD_REMOVE_ADMIN, DELETE_ADMIN, WRITE_NAME, SEND_PHONE, SETTINGS, UPDATE_NAME, UPDATE_PHONE
from callbacks import callback
from dotenv import load_dotenv
import os
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
TOKEN = os.environ.get('TOKEN')
updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher





create_conversation_handler = ConversationHandler(
    entry_points = [MessageHandler(Filters.text('Поиск лекарств🔎'), find_drug)],
    states = {
        # GET_BILL_DETAILS: [MessageHandler(Filters.text,get_bill_details)],
        GLOBAL_NAME: [MessageHandler(Filters.all, global_name)],
        SELECT_DRUGS: [MessageHandler(Filters.all, select_drugs)],
        
    },
    fallbacks = [CallbackQueryHandler(select_drugs)]
)
start_conversation_handler = ConversationHandler(
    entry_points = [CommandHandler('start', start)],
    states = {
        #GET_BILL_DETAILS: [MessageHandler(Filters.text,get_bill_details)],
        SUPERADMIN: [MessageHandler(Filters.text, superadmin)],
        UPDATE_EXCEL: [MessageHandler(Filters.all, update_excel)],
        EDIT_ABOUT_US: [MessageHandler(Filters.text, edit_about_us)],
        UPDATE_ABOUT_US: [MessageHandler(Filters.text, update_about_us)],
        
        EDIT_OUR_PARTNERS: [MessageHandler(Filters.text, edit_our_partners)],
        UPDATE_OUR_PARTNERS: [MessageHandler(Filters.document, update_our_partners)],
        EDIT_OUR_SITE: [MessageHandler(Filters.text, edit_our_site)],
        UPDATE_OUR_SITE: [MessageHandler(Filters.text, update_our_site)],
        CREATE_ADMIN: [MessageHandler(Filters.text, create_admin)],
        ADD_REMOVE_ADMIN: [MessageHandler(Filters.text, add_remove_admin)],
        DELETE_ADMIN: [MessageHandler(Filters.text, delete_admin)],
        WRITE_NAME: [MessageHandler(Filters.text, write_name)],
        SEND_PHONE: [MessageHandler(Filters.all, send_phone)],
    },
    fallbacks = [CallbackQueryHandler(cancel)]
)
setting_conversation_handler = ConversationHandler(
    entry_points = [MessageHandler(Filters.text(['Настройки⚙️', 'Вернуться к настройкам']), settings)],
    states = {
        SETTINGS: [MessageHandler(Filters.text, setting_menus)], 
        UPDATE_NAME: [MessageHandler(Filters.text, update_name)],
        UPDATE_PHONE: [MessageHandler(Filters.text, update_phone)],
    },
    fallbacks = []
)

dp.add_handler(setting_conversation_handler)
dp.add_handler(start_conversation_handler)
dp.add_handler(create_conversation_handler)

dp.add_handler(MessageHandler(Filters.document, doc))
dp.add_handler(CallbackQueryHandler(callback))
#menus

dp.add_handler(MessageHandler(Filters.text('О нас🧾'), about_us))
dp.add_handler(MessageHandler(Filters.text('Наши партнеры🤝'), our_partners))
dp.add_handler(MessageHandler(Filters.text('Наш сайт'), our_site))

dp.add_handler(MessageHandler(Filters.forwarded, forward))
updater.start_webhook(listen='127.0.0.1',
                      port=40404,
                      url_path=TOKEN)
    

updater.bot.set_webhook('https://aptekabot.elite-house.uz/{}'.format(TOKEN))