from datetime import datetime
import pymongo
import random
from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://monas:171718@cluster0.abcab19.mongodb.net/?retryWrites=true&w=majority") 
db = cluster["orders"]
mycol = db["orders"]
db_users = cluster["users"]
col_users = db_users["users"]
import logging
import os
from price import price_dict
PORT = int(os.environ.get('PORT', '8443'))
TOKEN = "5736521511:AAFmgKo6jhYSvvTbTaPFqU-dGZCXyop1b_M"
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

START, REGISTER, GENDER, PHOTO, AGAIN,LOCATION, BIO, FINISH = range(8)

item = []

total = 0
def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    user = update.message.from_user
    reply_keyboard = [['ቁርስ','ምሳ'],['ጁስ']]
    if (col_users.find_one({ 'chat_id': user['id']}) is not None):
        update.message.reply_text(
            'ሰላም! እንኳን ወደ ኮኪር ኪችን በሰላም መጡ'
            'ለጤናዎ ተስማሚ የሆኑ ምግቦችን እና መጠጦችን ለመምረጥ ከታች ያሉትን ቁልፎች ይጫኑ'
            ,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=False, input_field_placeholder='ምን እንታዘዝ?'
            ),
        )
        update.message.reply_photo(
            open('menu.png','rb')
           
        )
        return GENDER
    else:
       
        update.message.reply_text(
            'ሰላም! እንኳን ወደ ኮኪር ኪችን በሰላም መጡ'
            'ለተቀላጠፈ አገልግሎት እባክዎን'
            'ስልክ ቁጥሮን እና አድራሻዎን ያስገቡ (ኡራጎ ህንፃ 0912345678 )' , reply_markup=ReplyKeyboardRemove()
            
        )
        
        return REGISTER
    
def again(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    user = update.message.from_user
    reply_keyboard = [['ቁርስ','ምሳ'],['ጁስ','ኬክ']]
    update.message.reply_text(
            'ሌላ ትዕዛዝ ይምረጡ'

            ,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=False, input_field_placeholder='ምን እንታዘዝ?'
            ),
        )
    return GENDER
    
    
    
    
def register(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['ይቀጥሉ']]
    no = update.message.text
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    user = update.message.from_user
    mydict = { 
        "chat_id": user['id'],
        "username": user['username'],
        "is_bot": user['is_bot'],
        "first_name": user['first_name'],
        "last_name": user['first_name'], 
        "chat_id":user['id'], 
        "phone_number": no,
        "timestamp": dt_string }
    x = col_users.insert_one(mydict)
    logger.info("ትዕዛዝ %s:", user )
    update.message.reply_text( 'ስለተመዘገቡ እናመሰግናለን ለመቀጠል "ይቀጥሉ" የሚለውን ቁልፍ ይጫኑ', 
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False
        ), )
    return START

    

def gender(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    if (update.message.text=="ቁርስ"):
        reply_keyboard = [['ፉል ኖርማል','ፉል ስፔሻል', 'እንቁላል ፍርፍር'],['እንቁላል ስልስ','ፈታ ኖርማል', 'ፈታ ስፔሻል'],['ፈጢራ በማር','ፈጢራ በእንቁላል', 'ጨጨብሳ በማር'],['ጨጨብሳ በእንቁላል','እንጀራ ፍርፍር']]
        update.message.reply_text(
        'ካሉን ቁርሶች መካከል ይምረጡ',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder='ቁርስ ይምረጡ'
        ), )
    elif (update.message.text=="ምሳ"):
        
        reply_keyboard = [['በያይነት','ተጋቢኖ'],['ፓስታ በስጎ','ፓስታ በአትክልት'],['ሩዝ በስጎ','ሩዝ በአትክልት']]
        update.message.reply_text(
        'ካሉን ምሳዎች መካከል ይምረጡ',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder='ምሳ ይምረጡ'
        ), )
    elif (update.message.text=="ጁስ"):
        
        reply_keyboard = [['ማንጎ ጁስ','አቮካዶ ጁስ','አናናስ ጁስ'],['ፓፓያ ጁስ','ስፕሪስ ጁስ']]
        update.message.reply_text(
        'ካሉን ጁሶች መካከል ይምረጡ',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder='ጁስ ይምረጡ'
        ), )
    elif (update.message.text=="ኬክ"):
        
        reply_keyboard = [['ዶናት','ክሬም ኬክ']]
        update.message.reply_text(
        'ካሉን ኬኮች መካከል ይምረጡ',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder='ኬክ ይምረጡ'
        ), )
        
    logger.info("ትዕዛዝ %s: %s", str(user), update.message.text)
    

    return PHOTO



def photo(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['1','2'],['3','4']]
    """Stores the photo and asks for a location."""
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    user = update.message.from_user
    order = [user['id'],user['first_name'],user['last_name'], update.message.text]
    item.append({'meal':update.message.text, 'price': price_dict[update.message.text]})
    logger.info("Gender of %s: %s", str(total), update.message.text)

    update.message.reply_text(
        'ስንት %s ይሁንሎት' % update.message.text
        ,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder='ቁርስ፣ ምሳ ወይስ ጁስ?'
        ), )
    
    global u
    u = order
    return BIO


def bio(update: Update, context: CallbackContext) -> int:
    """Stores the info about the user and ends the conversation."""
    reply_keyboard = [['አዎ','አይ']]
    user = update.message.from_user
    item[-1].update({"amount": int(update.message.text)})  
    
    logger.info("order of %s", str(5))
    update.message.reply_text('ሌላ ትዕዛዝ አለዎት?',  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder='ቁርስ፣ ምሳ ወይስ ጁስ?'
        ),)

    return FINISH

def finish(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['ሌላ ትዕዛዝ']]
    if(update.message.text=='አዎ'):
        logger.info("User %s canceled the conversation.", update.message.text)
        update.message.reply_text(
        'ለመቀጠል "ሌላ ትዕዛዝ" የሚለውን ቁልፍ ይጫኑ', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder='ሌላ ትዕዛዝ'
        ),)
        return AGAIN

    else:
        global item
        total = 0
        for items in item:
            total = total + items['price']*items['amount']
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        user = update.message.from_user
        mydict = { 
        "_id": random.randrange(1545,9999),
        "first_name": user['first_name'], 
        "chat_id":user['id'], 
        "location": "Urago 78",
        "comment": "ቃርያ እንዳይገባ",
        "orders": item, 
        "phone_number": col_users.find_one({ 'chat_id': user['id']})['phone_number'],
        "total": total,
        "timestamp": dt_string }
        info = ""
        for items in item:
            info = "\n" + info + str(items['amount'])+" " + items['meal'] + "\n"

        x = mycol.insert_one(mydict)
        update.message.reply_text(
        'ትዕዛዝዎን  %s ተቀብለናል። \n አጠቃላይ ዋጋ %d ብር ብቻ። \n በ5 ደቂቃ ውስጥ እናደርሳለን። \n ለአዲስ ትዕዛዝ /start የሚለውን ይጫኑ' % ( info,  total), reply_markup=ReplyKeyboardRemove()
    )
        item = []
        total = 0
        return ConversationHandler.END
        
    

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'ትዕዛዙ ተሰርዟል! ለአዲስ ትዕዛዝ /start ን ይጫኑ', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5736521511:AAFmgKo6jhYSvvTbTaPFqU-dGZCXyop1b_M")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),],
        states={
            START: [MessageHandler(Filters.text & ~Filters.command, start), CommandHandler('start', start)],
            REGISTER: [MessageHandler(Filters.text & ~Filters.command, register), CommandHandler('start', start)],
            GENDER: [MessageHandler(Filters.regex('^(ቁርስ|ምሳ|ጁስ|ኬክ)$'), gender), CommandHandler('start', start)],
            PHOTO: [MessageHandler(Filters.text & Filters.regex('^(ማንጎ ጁስ|አቮካዶ ጁስ|ፓፓያ ጁስ|አናናስ ጁስ|ስፕሪስ ጁስ|ፉል ኖርማል|ፉል ስፔሻል|እንቁላል ፍርፍር|እንቁላል ስልስ|ፈታ ኖርማል|ፈታ ስፔሻል|ፈጢራ በማር|ፈጢራ በእንቁላል|ጨጨብሳ በማር|ጨጨብሳ በእንቁላል|እንጀራ ፍርፍር|በያይነት|ተጋቢኖ|ፓስታ በስጎ|ፓስታ በአትክልት|ሩዝ በስጎ|ሩዝ በአትክልት)$')  & ~Filters.command, photo), CommandHandler('start', start)],
            AGAIN: [MessageHandler(Filters.text  & ~Filters.command, again), CommandHandler('start', start)],
            FINISH: [MessageHandler(Filters.text  & ~Filters.command, finish), CommandHandler('start', start)],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio), CommandHandler('start', start)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN,
        webhook_url='https://kokirbot.herokuapp.com/' + TOKEN
    )

    updater.bot.setWebhook('https://kokirkitchen.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    


if __name__ == '__main__':
    main()
