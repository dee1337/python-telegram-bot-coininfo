import asyncio
import logging
import time
import asyncio
from telegram import Update, InputMediaDocument, InputMediaAudio
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def init_ath():
    """ non-async! returns inital ATH as float at start """
    response = requests.get(URL + 'bitcoin')
    soup = BeautifulSoup(response.text, 'html.parser')
    # Finden des Elements, das den ATH-Preis enthält
    ath_element = soup.find('div', class_='sc-f70bb44c-0 dVdjLB')
    ath_price = ath_element.find('span').text
    # ath_date = get_bitcoin_ath_date()
    # $-Zeichen entfernen
    ath_float = float(ath_price[1:].replace(',', ''))
    print("ath init:", ath_float)
    return ath_float


async def get_and_check_ath(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ returns True if ATH was raised, False otherwise """
    try:  #
        global last_ath_value
        response = requests.get(URL + 'bitcoin')
        soup = BeautifulSoup(response.text, 'html.parser')
        ath_element = soup.find('div', class_='sc-f70bb44c-0 dVdjLB')
        ath_price = float(ath_element.find('span').text[1:].replace(',', ''))

        if last_ath_value < ath_price:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="DingDingDing! New ATH: ${:.2f} -> ${:.2f}".format(last_ath_value, ath_price ))
            print(f"{last_ath_value} < {ath_price}:")
            last_ath_value = ath_price
            return True  # New ATH detected
        else:
            return False  # Not a new ATH

    except Exception as e:
        print(f"Error occurred: {e}")
        return None  # Handle error


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ show all available BOT commands """
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""
    These commands are currently available:

    /start - starts the bot (already done for you ;-))
    /help - shows this
    /last - shows the BTC ATH in $
    /watch - status of monitoring BTC-ATH
    /fake - fakes the ATH with +1337
    /reset - resets the ATH to realtime data
    /realtime - execute watching
    """)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ writes an introductional message from the bot """
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="I'm Satoshi, please trust me by DMing me your private keys!")
async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ writes an introductional message from the bot """
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Am i watching for BTC already? "+str(WATCHING))

async def fake_ath(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ writes an introductional message from the bot """
    global last_ath_value
    last_ath_value += 1337
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Faking ATH: Setting ATH to $"+str(last_ath_value))

async def reset_ath(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ writes an introductional message from the bot """
    global last_ath_value
    last_ath_value = init_ath()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Resetting ATH to live data: $"+str(last_ath_value))
async def pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ send media"""
    await context.bot.send_document(chat_id=update.effective_chat.id, document='media/btc001.png')
async def media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ send media"""
    media_1 = InputMediaDocument(media=open('media/btc001.png', 'rb'))
    media_2 = InputMediaDocument(media=open('media/ratschbing.mp3', 'rb'))
    await context.bot.send_media_group(chat_id=update.effective_chat.id, media=[media_1, media_2])
async def audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ send audio"""
    # await update.message.reply_audio(audio='media/ratschbing.mp3') # quotet mich dann!
    await update.message.reply_voice(voice='media/ratschbing.mp3', caption="ATH-Test")
    # await context.bot.send_audio(chat_id=update.effective_chat.id, document='media/ratschbing.mp3')

async def getCurrentATH(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ shows the current ATH + ATH Date"""
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Last BTC ATH: $" + str(last_ath_value))
async def main_loop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("started main loop")
    print(f"started at {time.strftime('%X')}")
    while True:
        global WATCHING
        WATCHING = True
        print(f"\tLOOP started at {time.strftime('%X')}")
        new_ath = await get_and_check_ath(Update, ContextTypes.DEFAULT_TYPE)
        if new_ath:
            print("\tNew ATH detected!")
        else:
            print("\tNo new ATH this time.")
        await asyncio.sleep(10)
    print(f"finished at {time.strftime('%X')}")



if __name__ == '__main__':
    load_dotenv()
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    WATCHING = False
    URL = 'https://coinmarketcap.com/currencies/'  # URL for the Bitcoin page on CoinMarketCap
    last_ath_value = init_ath()
    print("pre main():", last_ath_value)

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', cmd_help)
    application.add_handler(help_handler)

    lastATH_handler = CommandHandler('last', getCurrentATH)
    application.add_handler(lastATH_handler)

    fakeATH_handler = CommandHandler('fake', fake_ath)
    application.add_handler(fakeATH_handler)

    resetATH_handler = CommandHandler('reset', reset_ath)
    application.add_handler(resetATH_handler)

    watch_handler = CommandHandler('watch', watch)
    application.add_handler(watch_handler)

    # UNDOCUMENTED (in help) STUFF #

    # not tested yet
    pic_handler = CommandHandler('pic', pic)
    application.add_handler(pic_handler)

    audio_handler = CommandHandler('audio', audio)
    application.add_handler(audio_handler)

    media_handler = CommandHandler('media', media)
    application.add_handler(media_handler)

    realtime_handler = CommandHandler('realtime', main_loop)
    application.add_handler(realtime_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
    #asyncio.run(main())




