import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import yfinance as yf
import pandas as pd

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token
TOKEN = '8699821370:AAEQUSbLTgf7MmWqo5vV5LHPOz30wfqOfqw'

# Stock Analysis Functions

def get_stock_price(symbol: str) -> float:
    stock = yf.Ticker(symbol)
    return stock.history(period='1d')['Close'].iloc[-1]


def analyze_stock(symbol: str) -> str:
    price = get_stock_price(symbol)
    return f'The current price of {symbol} is {price:.2f}'

# Command Handlers

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Stock Trading Bot!')


def price(update: Update, context: CallbackContext) -> None:
    if context.args:
        symbol = context.args[0]
        analysis = analyze_stock(symbol)
        update.message.reply_text(analysis)
    else:
        update.message.reply_text('Please provide a stock symbol!')

# Main function to start the bot

def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('price', price))

    updater.start_polling()  
    updater.idle()

if __name__ == '__main__':
    main()