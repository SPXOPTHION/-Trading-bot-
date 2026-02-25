import logging
import os
import yfinance as yf
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Set the logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the commands functions

# Start Command
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton('CALL', callback_data='call'), InlineKeyboardButton('PUT', callback_data='put')],
                [InlineKeyboardButton('SCAN', callback_data='scan'), InlineKeyboardButton('INFO', callback_data='info')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('مرحبا بك في بوت تداول الأسهم! اختر أحد الأزرار أدناه:', reply_markup=reply_markup)

# Callback function for button presses

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'call':
        query.edit_message_text(text='لقد اخترت CALL. أدخل رمز السهم:')
        context.user_data['action'] = 'call'
    elif query.data == 'put':
        query.edit_message_text(text='لقد اخترت PUT. أدخل رمز السهم:')
        context.user_data['action'] = 'put'
    elif query.data == 'scan':
        query.edit_message_text(text='بوظيفة SCAN. أدخل فترة التحليل:')
        context.user_data['action'] = 'scan'
    elif query.data == 'info':
        query.edit_message_text(text='أدخل رمز السهم للحصول على معلومات السوق:')

# Function to handle stock symbol input

def handle_message(update: Update, context: CallbackContext) -> None:
    action = context.user_data.get('action')
    symbol = update.message.text.upper()

    if action in ['call', 'put']:
        # Perform CALL or PUT actions
        analyze_stock(symbol, action, update)
    elif action == 'scan':
        # Scan functionality
        scan_stocks(update)
    elif action == 'info':
        # Info functionality
        stock_info(symbol, update)
    # Reset action
    context.user_data['action'] = None

# Analyze stock for CALL/PUT

def analyze_stock(symbol: str, action: str, update: Update) -> None:
    try:
        stock_data = yf.Ticker(symbol)
        current_price = stock_data.history(period='1d')['Close'].iloc[-1]
        sma = stock_data.history(period='20d')['Close'].rolling(window=20).mean().iloc[-1]
        if (action == 'call' and current_price > sma) or (action == 'put' and current_price < sma):
            update.message.reply_text(f'سعر {symbol} الحالي هو {current_price}. استثمار {action} محسوب. SMA: {sma}.')
        else:
            update.message.reply_text(f'الاتجاه ليس مناسبًا للاستثمار {action} في {symbol}.')
    except Exception as e:
        logger.error(f'Error in analyze_stock: {e}')
        update.message.reply_text('خطأ: لم أتمكن من الحصول على بيانات السهم.')

# Scan stocks function

def scan_stocks(update: Update) -> None:
    # Placeholder for stock scanning functionality
    update.message.reply_text('تفحص الأسهم جاري المعالجة...')

# Stock info function

def stock_info(symbol: str, update: Update) -> None:
    try:
        stock_data = yf.Ticker(symbol)
        info = stock_data.info
        update.message.reply_text(f'معلومات {symbol}: {info}')
    except Exception as e:
        logger.error(f'Error in stock_info: {e}')
        update.message.reply_text('خطأ: لم أتمكن من الحصول على معلومات السهم.')

# Main function

def main() -> None:
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Make sure to set your token as an environment variable
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()