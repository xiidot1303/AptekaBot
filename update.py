from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from bot import start, global_name, select_drugs, doc, cancel, error, find, update_excel, forward
from buttons import find_drug, about_us, our_partners, our_site, settings
from admin import superadmin, edit_about_us, update_about_us, edit_our_partners, update_our_partners, edit_our_site, update_our_site, create_admin, add_remove_admin
from conversationList import GLOBAL_NAME, SELECT_DRUGS, SUPERADMIN, UPDATE_EXCEL, START, EDIT_ABOUT_US, UPDATE_ABOUT_US, EDIT_OUR_PARTNERS, UPDATE_OUR_PARTNERS, EDIT_OUR_SITE
from conversationList import UPDATE_OUR_SITE, CREATE_ADMIN, ADD_REMOVE_ADMIN

TOKEN = '1415026630:AAG7eTqgeNy0sHu2KUHiLvigsgyLcJ-aXKw'

updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_error_handler(error)



create_conversation_handler = ConversationHandler(
    entry_points = [MessageHandler(Filters.text('Поиск лекарств'), find_drug)],
    states = {
        # GET_BILL_DETAILS: [MessageHandler(Filters.text,get_bill_details)],
        GLOBAL_NAME: [MessageHandler(Filters.text, global_name)],
        SELECT_DRUGS: [MessageHandler(Filters.text, select_drugs)],
        
    },
    fallbacks = [CommandHandler('cancel', cancel)]
)
start_conversation_handler = ConversationHandler(
    entry_points = [CommandHandler('start', start)],
    states = {
        #GET_BILL_DETAILS: [MessageHandler(Filters.text,get_bill_details)],
        SUPERADMIN: [MessageHandler(Filters.text, superadmin)],
        UPDATE_EXCEL: [MessageHandler(Filters.document, update_excel)],
        EDIT_ABOUT_US: [MessageHandler(Filters.text, edit_about_us)],
        UPDATE_ABOUT_US: [MessageHandler(Filters.text, update_about_us)],
        START: [CommandHandler('start', start)],
        EDIT_OUR_PARTNERS: [MessageHandler(Filters.text, edit_our_partners)],
        UPDATE_OUR_PARTNERS: [MessageHandler(Filters.text, update_our_partners)],
        EDIT_OUR_SITE: [MessageHandler(Filters.text, edit_our_site)],
        UPDATE_OUR_SITE: [MessageHandler(Filters.text, update_our_site)],
        CREATE_ADMIN: [MessageHandler(Filters.text, create_admin)],
        ADD_REMOVE_ADMIN: [MessageHandler(Filters.text, add_remove_admin)],
    },
    fallbacks = [CommandHandler('cancel', cancel)]
)

dp.add_handler(start_conversation_handler)
dp.add_handler(create_conversation_handler)

dp.add_handler(MessageHandler(Filters.document, doc))
#menus

dp.add_handler(MessageHandler(Filters.text('О нас'), about_us))
dp.add_handler(MessageHandler(Filters.text('Наши партнеры'), our_partners))
dp.add_handler(MessageHandler(Filters.text('Наш сайт'), our_site))
dp.add_handler(MessageHandler(Filters.text('Настройки'), settings))
dp.add_handler(MessageHandler(Filters.forwarded, forward))
updater.start_polling()
