import asyncio
import logging
import time
import asyncio
from telegram import Update, InputMediaDocument, InputMediaAudio
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import os
from dotenv import load_dotenv
import coinmarketcap

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WATCHING = False

# Variable zum Speichern des zuletzt gespeicherten ATH-Preises
last_ath_value = coinmarketcap.get_bitcoin_ath()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm Satoshi, please trust me by DMing me your private keys!")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ show all available commands """
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""
    These commands are currently available:
    
    /start - starts the bot (already done for you ;-))
    /help - shows this
    /last - shows the BTC ATH in $
    /watch - start watching for BTC-ATH
    """)

async def getCurrentATH(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ shows the current ATH + ATH Date"""
    last_ath_date = coinmarketcap.get_bitcoin_ath_date()
    bitcoin_hi = coinmarketcap.get_bitcoin_ath()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Last BTC ATH ($"+str(bitcoin_hi)+") was on "+last_ath_date)

async def pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ send media"""
    #await context.bot.send_message(chat_id=update.effective_chat.id, text="Last BTC ATH ($"+str(bitcoin_hi)+") was on "+last_ath)
    await context.bot.send_document(chat_id=update.effective_chat.id, document='media/btc001.png')

async def media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ send media"""
    #await context.bot.send_message(chat_id=update.effective_chat.id, text="Last BTC ATH ($"+str(bitcoin_hi)+") was on "+last_ath)
    #await context.bot.send_document(chat_id=update.effective_chat.id, document='media/ratschbing.mp3')

    media_1 = InputMediaDocument(media=open('media/btc001.png', 'rb'))
    media_2 = InputMediaDocument(media=open('media/ratschbing.mp3', 'rb'))
    await context.bot.send_media_group(chat_id=update.effective_chat.id, media=[media_1, media_2])

async def audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ send audio"""
    ## await context.bot.send_document(chat_id=update.effective_chat.id, document='media/ratschbing.mp3')
    # await update.message.reply_audio(audio='media/ratschbing.mp3') # quotet mich dann!
    await update.message.reply_voice(voice='media/ratschbing.mp3',caption="ATH-Test")
    #await context.bot.send_audio(chat_id=update.effective_chat.id, document='media/ratschbing.mp3')

async def watch_ath(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_ath_value
    print("WATCHING:", WATCHING)
    if (WATCHING):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="already watching for ATH!")
        return
    await context.bot.send_message(chat_id=update.effective_chat.id, text="started watching ATH (60 sec frequency)")
    update_rate = 60
    async def watch_ath_loop():
        # Schleife für die periodische Überprüfung
        while True:
            current_ath = coinmarketcap.get_bitcoin_ath() #-10000 #-10000 = MOCK
            # Überprüfen, ob sich der ATH-Preis geändert hat
            if current_ath > last_ath_value:
                bitcoin_hi = coinmarketcap.get_bitcoin_ath()
                last_ath = coinmarketcap.get_bitcoin_ath_date()
                bitcoin_hi = coinmarketcap.get_bitcoin_ath()
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text="DingDingDing! New BTC ATH: $" + str(bitcoin_hi) + " (" + last_ath + ")")
                #await context.bot.send_message(chat_id=update.effective_chat.id, text="Last BTC ATH ($" + str(bitcoin_hi) + ") was on " + last_ath)

                print(f'Bitcoin ATH hat sich geändert! Von {last_ath_value} zum neuen ATH: ${current_ath}')
                last_ath_value = bitcoin_hi
                print(f'Bitcoin ATH hat sich geändert am {current_ath}')
            else:
                print('Bitcoin ATH hat sich nicht geändert.')

            # Wartezeit für 1 Minute
            await asyncio.sleep(update_rate)  # jede Minute mal schauen
    asyncio.create_task(watch_ath_loop())

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    lastATH_handler = CommandHandler('last', getCurrentATH)
    application.add_handler(lastATH_handler)

    watch_handler = CommandHandler('watch', watch_ath)
    application.add_handler(watch_handler)


    ## UNDOCUMENTED STUFF ##

    # not tested yet
    pic_handler = CommandHandler('pic', pic)
    application.add_handler(pic_handler)

    audio_handler = CommandHandler('audio', audio)
    application.add_handler(audio_handler)

    media_handler = CommandHandler('media', media)
    application.add_handler(media_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)