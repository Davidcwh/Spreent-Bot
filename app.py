import logging
import time
import os

from telegram import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup)
import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# State definitions for top level conversation
SELECTING_ACTION, CREATING_SPREE, SEARCH_SPREE, SEARCHING, USER_SPREES, START_CREATE_SPREE= map(chr, range(6))
# State definitions for second level conversation
SAVE_SPREE, CREATE_SPREE_MENU = map(chr, range(6, 8))
# State definitions for descriptions conversation
SELECTING_FIELD, TYPING_FIELD, RETURN_MAIN = map(chr, range(8, 11))
# Meta states
STOPPING, SHOWING = map(chr, range(10, 12))
# Shortcut for ConversationHandler.END
END = ConversationHandler.END

# Different constants for this example
(PARENTS, CHILDREN, SELF, CURRENT, MALE, FEMALE, MIN, NAME, START_OVER, FEATURES,
 CURRENT_FEATURE, CURRENT_LEVEL) = map(chr, range(10, 22))

global bot
global TOKEN
TOKEN = '1047562188:AAGQPtjyCzNn6lHMc-obwmRR7CBfXoz5QYQ'
#TOKEN = os.environ.get('TOKEN')
bot = telegram.Bot(TOKEN)


# Top level conversation callbacks
def start(update, context):
    welcome_text = 'Welcome to Spreent! Connect with other online shoppers to hit minimum free shipping'
    followup_text = 'What would you like to do today?\nTo abort, simply type /stop.'
    buttons = [[
        InlineKeyboardButton(text='Create a new Spree ✍️', callback_data=str(START_CREATE_SPREE))
    ], [
        InlineKeyboardButton(text='Search for Spree 🔍', callback_data=str(SEARCH_SPREE))
    ], [
        InlineKeyboardButton(text='My Sprees', callback_data=str(USER_SPREES))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    
    # If we're starting over we don't need do send a new message
    if context.user_data.get(START_OVER):
        update.callback_query.edit_message_text(text=followup_text, reply_markup=keyboard)
    else:
        update.message.reply_text(text=welcome_text)
        update.message.reply_text(text=followup_text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECTING_ACTION


def search_spree(update, context):
     text = 'Type what you are looking for:\n\nE.g. Name of website you are shopping at'
     update.callback_query.edit_message_text(text=text)

     return SEARCHING

def search_results(update, context):
     search_input = update.message.text
     buttons = [[
        InlineKeyboardButton(text='Back', callback_data=str(END))
    ]]

     keyboard = InlineKeyboardMarkup(buttons)
     update.message.reply_text(text='Displaying spreent results from your search of \"' + search_input + '\":\n', reply_markup=keyboard)

     # get results from database here and display them somehow
     
     context.user_data[START_OVER] = True
     return SHOWING



def start_create_spree(update, context):
    text = 'A Spree has 3 essential fields:\nName, Minimum Free Shipping Amount, Current Amount\n\nAll 3 fields must be entered when creating your new Spree.'
    button = InlineKeyboardButton(text='Okay got it!', callback_data=str(CREATE_SPREE_MENU))
    keyboard = InlineKeyboardMarkup.from_button(button)

    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return CREATING_SPREE

def create_spree_menu(update, context):
    """Select a Spree field to enter """
    buttons = [[
        InlineKeyboardButton(text='Name', callback_data=str(NAME))
    ], [
        InlineKeyboardButton(text='Min Spending Amount', callback_data=str(MIN))
    ], [
        InlineKeyboardButton(text='Add current amount', callback_data=str(CURRENT)),
    ], [
        InlineKeyboardButton(text='Done', callback_data=str(END)),
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    # if it is the first time we are navigating to this menu
    if not context.user_data.get(START_OVER):
        text = 'Please select a field to update.'
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else: # Else, give acknowledgement message
        text = 'Got it! Please select a feature to update.'
        update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECTING_FIELD

def ask_for_input(update, context):
    field = 'field'
    if update.callback_query.data == NAME:
        field = 'name'
    elif update.callback_query.data == MIN:
        field = "Minimum Spending Amount"
    elif update.callback_query.data == CURRENT:
        field = "current amount"
    text = 'Okay, tell me your Spree\'s ' + field
    update.callback_query.edit_message_text(text=text)
    return TYPING_FIELD

def validate_input(update, context):
    text = update.message.text
    #validate input here
    context.user_data[START_OVER] = True
    return create_spree_menu(update, context)

def save_spree(update, context):
    #retrieve saved fields and save it into database
    text = 'Spree name:\nMin Spending Amount:\nCurrent Amount:\n\nSpree saved!✅'
    
    buttons = [[
        InlineKeyboardButton(text='Okay', callback_data=str(END))
    ]]

    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    
    # get results from database here and display them somehow
    context.user_data[START_OVER] = True
    return SHOWING

def display_user_sprees(update, context):
    buttons = [[
        InlineKeyboardButton(text='Back', callback_data=str(END))
    ]]

    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text='Here are the Sprees you have joined/created:', reply_markup=keyboard)

     # get results from database here and display them somehow
     
    context.user_data[START_OVER] = True
    return SHOWING


def stop(update, context):
    """End Conversation by command."""
    update.message.reply_text('Okay, bye.')

    return END

def stop_nested(update, context):
    """Completely end conversation from within nested conversation."""
    update.message.reply_text('Okay, bye.')

    return STOPPING

def end(update, context):
    """End conversation from InlineKeyboardButton."""
    text = 'See you around!'
    update.callback_query.edit_message_text(text=text)

    return END

# Error handler
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SHOWING: [CallbackQueryHandler(start, pattern='^' + str(END) + '$')],
            SELECTING_ACTION: [
                CallbackQueryHandler(search_spree, pattern='^' + str(SEARCH_SPREE) + '$'),
                CallbackQueryHandler(start_create_spree, pattern='^' + str(START_CREATE_SPREE) + '$'),
                CallbackQueryHandler(display_user_sprees, pattern='^' + str(USER_SPREES) + '$'),
            ],
            SEARCHING: [MessageHandler(Filters.text, search_results)],
            CREATING_SPREE:[CallbackQueryHandler(create_spree_menu, pattern='^' + str(CREATE_SPREE_MENU) + '$'),],
            SELECTING_FIELD: [
                CallbackQueryHandler(ask_for_input, pattern='^(?!' + str(END) + ').*$'),
                CallbackQueryHandler(save_spree, pattern='^' + str(END) + '$')
            ],
            TYPING_FIELD: [
                MessageHandler(Filters.text, validate_input),
            ],
        },

        fallbacks=[
            CommandHandler('stop', stop)
        ],
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    
if __name__ == '__main__':
    main()