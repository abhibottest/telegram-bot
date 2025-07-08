
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yfinance as yf

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('👋 Hello! I am your bot. Send me anything and I will echo it.')

# echo handler
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

# /markets command handler
def markets(update: Update, context: CallbackContext) -> None:
    tickers = {
        "^GSPC": "S&P 500",
        "^DJI": "Dow Jones",
        "^IXIC": "NASDAQ",
        "^FTSE": "FTSE 100",
        "^N225": "Nikkei 225",
        "^HSI": "Hang Seng",
        "^GDAXI": "DAX"
    }
    data = yf.download(tickers=list(tickers.keys()), period="1d", interval="1m")
    latest = data['Close'].iloc[-1]
    msg_lines = ["📈 *Global Market Indices:*"]
    for symbol, name in tickers.items():
        price = latest[symbol]
        msg_lines.append(f"{name}: {price:.2f}")
    update.message.reply_text('\n'.join(msg_lines), parse_mode='Markdown')

def main() -> None:
    # Replace this token with yours
    TOKEN = "YOUR_BOT_TOKEN"
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("markets", markets))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
