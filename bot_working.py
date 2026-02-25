import yfinance as yf
import pandas as pd
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Initialize your Telegram bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Initialize the updater and dispatcher
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

# Function to get stock data and perform trading analysis
def analyze_stocks(stock_symbols):
    signals = {}
    for symbol in stock_symbols:
        data = yf.download(symbol, period="1mo", interval="1d")
        data['SMA20'] = data['Close'].rolling(window=20).mean()
        data['SMA50'] = data['Close'].rolling(window=50).mean()
        
        last_row = data.iloc[-1]
        if last_row['SMA20'] > last_row['SMA50']:
            signals[symbol] = 'BUY'
        elif last_row['SMA20'] < last_row['SMA50']:
            signals[symbol] = 'SELL'
        else:
            signals[symbol] = 'HOLD'
    return signals

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("CALL", callback_data='call')],
        [InlineKeyboardButton("PUT", callback_data='put')],
        [InlineKeyboardButton("SCAN", callback_data='scan')],
        [InlineKeyboardButton("INFO", callback_data='info')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose an option:', reply_markup=reply_markup)

# Callback query handler
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data == 'scan':
        signals = analyze_stocks(['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA'])
        response = '\n'.join([f"{symbol}: {signal}" for symbol, signal in signals.items()])
        query.edit_message_text(text=f"Trading Signals:\n{response}")

# On every message
def main():
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    
    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()