import os
import logging

from telegram.ext import Updater,CommandHandler,MessageHandler,ConversationHandler,Filters
from telegram import ReplyKeyboardMarkup
from random import randint

TOKEN = "1415026630:AAG7eTqgeNy0sHu2KUHiLvigsgyLcJ-aXKw"


ADD_ITEMS, FINAL_OR_MAKE_CHANGES, ADD_OR_DELETE, DELETE, STOP = range(5)

bill_items = []
ID = None


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
    message = "Welcome to the Bill Splitter Bot. An easy way to split bills among friends. The following are a list of"
    + "commands you can use."
    bot.send_message(chat_id=update.message.chat_id, text=message)
    message = ""
    message += "/help - To get a list of commands\n"
    message += "/create - To create a new bill\n"
    message += "/add - To add items spent on for a particular bill"
    message += "/get - To get the amount owed"

def create(bot, update):
    global ID

    message = "Hey! Looks like you're trying to create a new bill! One moment, while I create a new ID for you!"

    bot.send_message(chat_id=update.message.chat_id, text=message)

    id_for_bill = randint(1000,9999)

    # Check if bill id does not exist in database
    message = "Here's the ID for your bill: " + str(id_for_bill)
    ID = id_for_bill
    print(ID)
    bot.send_message(chat_id=update.message.chat_id, text=message)

    message = "Can you enter the items followed by the price for the bill? A simple format would look as follows. Type "
    message += "Done when you're done adding items to the bill\n"
    bot.send_message(chat_id=update.message.chat_id, text=message)

    message = " <pre>Pizza        - 150\n"
    message += "Pasta        - 150\n"
    message += "Garlic Bread - 230</pre> "
    reply_keyboard = [["Done"]]

    bot.send_message(chat_id=update.message.chat_id, text=message,parse_mode="html")

    return ADD_ITEMS


def add_items_to_bill(bot, update):
    user_input_bill_items = update.message.text

    # Use regex
    if user_input_bill_items == "Done":
        message = "Looks like you're done! Here's your bill for re-confirmation: "

        item_count=0
        for item in bill_items:
            item_count += 1
            message += "<pre>" + str(item_count) + ". " + str(item) + "\n</pre>"
        bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode="html")

        message = "Do you want to make any changes to the bill?"
        reply_keyboard = [["Yes","No"]]
        bot.send_message(chat_id=update.message.chat_id, text=message, reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))

        return FINAL_OR_MAKE_CHANGES

    bill_items.append(user_input_bill_items)

    return ADD_ITEMS

def final_or_make_changes_to_bill(bot, update):
    user_choice_make_changes = update.message.text
    if user_choice_make_changes == "Yes":
        reply_keyboard = [["Add","Delete"]]
        message = "Do you want to add or delete?"
        bot.send_message(chat_id=update.message.chat_id, text=message, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ADD_OR_DELETE

    return STOP

def add_or_delete(bot, update):
    user_choice_add_or_delete = update.message.text

    if user_choice_add_or_delete == "Add":
        message = "Enter items you want to add."
        bot.send_message(chat_id=update.message.chat_id, text=message)

        return ADD_ITEMS

    message = "Enter the list number of the item you want to delete. Type Done when you're done."
    bot.send_message(chat_id= update.message.chat_id, text=message)

    return DELETE

def delete_item_from_bill(bot, update):
    number_to_delete = update.message.text
    print(number_to_delete)
    # SQL command to delete from table

    print("to be filled")

    return STOP

def stop(bot, update):
    print("ht")
    bot.send_message(chat_id=update.message.chat_id,text="dsfdsfsadf")
    return ConversationHandler.END

# def done(bot, update):
#     global ID 

#     bot.send_message(chat_id=update.message.chat_id, text="done")
#     print("done")

#     message = "Great! Share this ID with the other participants of the bill: "
#     bot.send_message(chat_id=update.message.chat_id, text=message)
#     return ConversationHandler.END



def cancel(bot,update):
    print("cancel")
    return ConversationHandler.END

def add_bought_items(bot, update):
    message = "Add the list of items conforming to this example. Bill followed by ID\nEg: 4632 1,2,3"
    bot.send_message(chat_id=update.message.chat_id, text=message)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, update.error)

def main():
    updater = Updater(TOKEN)
    db.setup()
    PORT = int(os.environ.get('PORT','8443'))
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help",start))

    create_conversation_handler = ConversationHandler(
        entry_points = [CommandHandler('create',create)],

        states = {
            # GET_BILL_DETAILS: [MessageHandler(Filters.text,get_bill_details)],

            ADD_ITEMS: [MessageHandler(Filters.text, add_items_to_bill)],

            FINAL_OR_MAKE_CHANGES: [MessageHandler(Filters.text, final_or_make_changes_to_bill)],

            ADD_OR_DELETE: [MessageHandler(Filters.text, add_or_delete)],

            DELETE: [MessageHandler(Filters.text, delete_item_from_bill)],

            STOP: [MessageHandler(Filters.text, stop)]

        },

        fallbacks = [CommandHandler('cancel',cancel)]
    )
    dp.add_handler(create_conversation_handler)
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler("add",add_bought_items))
    # dp.add_handler(CommandHandler("add",add))
    updater.start_polling()

if __name__ == "__main__":
    main()