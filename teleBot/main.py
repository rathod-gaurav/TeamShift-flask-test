import Constants as keys
from telegram.ext import *
import Responses as R

print("Bot Started...")

def start_command(update, context):
    update.message.reply_text('Type something random to get response!')

def help_command(update, context):
    update.message.reply_text('Go to http://shift.piviz.cc for any help')

def handle_message(update, context):
    text = str(update.message.text).lower()
    response = R.sample_responses(text)

    update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(Commandhandler("start", start_command))
    dp.add_handler(Commandhandler("start", help_command))

    dp.add_handler(Messagehandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling(60)
    updater.idle()

main()
    
    