from typing import Final
import logging
from telegram import Update
import telegram
from telegram.ext import ApplicationBuilder, CommandHandler,\
MessageHandler, filters, ContextTypes, CallbackContext,\
ConversationHandler, CallbackQueryHandler
import requests
import telebot
from telebot import types
import datetime


TELE_API: Final = "https://api.telegram.org/bot"
TOKEN: Final = "7201420993:AAFtlKvF0yVRxziBN1MIJ-o-TCq7CA01GEM"

KANGA_API: Final = "https://api.kanga.exchange"
asset_list = "/api/v2/market/assets"
market_tickers = "/api/v2/market/ticker"

get_updates = "/getUpdates"
send_message = "/sendMessage"

BOT_USERNAME: Final = "@erkanguro_bot"

# stages of conversation
MENU, LANG, ASSETS, PRICES, CHAT, ILE = range(6)


# for debugging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# it is called every time the bot receives a msg containing /start cmd
async def start_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    select_from = {}
    select_from['en'] = 'select from the options below'
    select_from['it'] = 'scegli dalle seguenti opzioni'
    select_from['de'] = 'Wähle aus diese Opzionen'
    select_from['ru'] = 'Выбери из следующих вариантов'
    select_from['pl'] = 'Wybierz z poniższych opcji'

    change_lang = {}
    change_lang['en'] = 'change the language'
    change_lang['it'] = 'cambia la lingua'
    change_lang['de'] = 'ändere die Sprache'
    change_lang['ru'] = 'измени язык'
    change_lang['pl'] = 'zmień język'
    
    asset_list = {}
    asset_list['en'] = 'asset list'
    asset_list['it'] = 'lista delle valute'
    asset_list['de'] = 'Liste der Währungen'
    asset_list['ru'] = 'листа валют'
    asset_list['pl'] = 'lista walut'

    prices = {}
    prices['en'] = 'prices'
    prices['it'] = 'prezzi'
    prices['de'] = 'Preise'
    prices['ru'] = 'цены'
    prices['pl'] = 'ceny'

    chat_with = {}
    chat_with['en'] = 'chat with er Kanguro'
    chat_with['it'] = 'chatta con er Kanguro'
    chat_with['de'] = 'schreib er Kanguro'
    chat_with['ru'] = 'пиши эр Кангуро'
    chat_with['pl'] = 'napisz do er Kanguro'
    
    download_wallet = {}
    download_wallet['en'] = 'download the wallet'
    download_wallet['it'] = 'scarica il portafoglio'
    download_wallet['de'] = 'lade die Brieftasche herunter'
    download_wallet['ru'] = 'скачай портфель'
    download_wallet['pl'] = 'pobierz portfel'

    initial_msg = 'select from the options below'
    change_language = 'change the language'
    asset_l = 'asset list'
    pri = 'prices'
    chat = 'chat with er Kanguro'
    download = 'download the wallet'
    
    '''
    if not update.callback_query:
        pass
    elif update.callback_query.data == 'lang' or 'assets' or 'prices' or 'chat':
        await button_func(update, context)
        return
    '''
    
    if update.callback_query and (update.callback_query.data == 'en' or 'it' or 'de' or 'ru' or 'pl'):
        initial_msg = select_from[update.callback_query.data]
        change_language = change_lang[update.callback_query.data]
        asset_l = asset_list[update.callback_query.data]
        pri = prices[update.callback_query.data]
        chat = chat_with[update.callback_query.data]
        download = download_wallet[update.callback_query.data]

    btn1 = telegram.InlineKeyboardButton(change_language, callback_data='lang')
    btn2 = telegram.InlineKeyboardButton(asset_l, callback_data='assets')
    btn3 = telegram.InlineKeyboardButton(pri, callback_data='prices')
    btn4 = telegram.InlineKeyboardButton(chat, callback_data='chat')
    btn5 = telegram.InlineKeyboardButton(download, callback_data='portfel')

    initial_keyboard = [[btn1, btn2], [btn3, btn4], [btn5]]
    reply_markup = telegram.InlineKeyboardMarkup(initial_keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=initial_msg,
        reply_markup=reply_markup
    )
    return MENU

async def button_func(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'lang':
        msg = 'click a button to select a language'
        btn1 = telegram.InlineKeyboardButton('Italian - Italiano', callback_data='it')
        btn2 = telegram.InlineKeyboardButton('German - Deutsch', callback_data='de')
        btn3 = telegram.InlineKeyboardButton('Russian - Русский', callback_data='ru')
        btn4 = telegram.InlineKeyboardButton('Polish - Polski', callback_data='pl')
        btn5 = telegram.InlineKeyboardButton('English', callback_data='en')
        lang_keyboard = [[btn1, btn2], [btn3, btn4], [btn5]]
        reply_markup = telegram.InlineKeyboardMarkup(lang_keyboard)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=msg,
            reply_markup=reply_markup
        )
        return LANG
    elif query.data == 'assets':
        a = get_assets()
        lista = [f'{x}    {a[x]["name"]}\n' for x in a.keys()]
        msg = [f'The list consists of {len(lista)} available assets: \n'] + lista
        msg = ''.join(msg)
        print(len(msg))
        i = 0
        step = 4096
        while i < len(msg):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=msg[i:i+step] if i+step < len(msg) else msg[i:len(msg)],
                )
            i += step
        return ASSETS
    elif query.data == 'prices':
        msg = 'Type the ticker of the asset You want to know the price of' + \
        '\nYou have 10 seconds!'
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=msg
        )
        now = datetime.datetime.now()
        deadline = now + datetime.timedelta(seconds=10)
        done = False
        while datetime.datetime.now() < deadline:
            the_ticker = read_msg(update.effective_chat.id)
        #wait 3 sec
        now2 = datetime.datetime.now()
        deadline2 = now2 + datetime.timedelta(seconds=3)
        while datetime.datetime.now() < deadline2:
            pass
        
        # buy or sell
        buy_btn = telegram.InlineKeyboardButton(f'buy {the_ticker}', callback_data=f'buy {the_ticker}')
        sell_btn = telegram.InlineKeyboardButton(f'sell {the_ticker}', callback_data=f'sell {the_ticker}')
        bs_keyboard = [[buy_btn, sell_btn]]
        reply_markup = telegram.InlineKeyboardMarkup(bs_keyboard)
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='buy or sell',
            reply_markup=reply_markup
        )
        
        return PRICES
    elif query.data == 'chat':
        msg = 'Click t.me/erkanguro to start the chat.'
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=msg
        )
    elif query.data == 'portfel':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='https://play.google.com/store/apps/details/Kanga_Wallet?id=com.kangamobile&hl=en_US&pli=1'
        )
        return
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='unknown option selected'
        )

async def buy_or_sell_func(update: Update, context: CallbackContext):

    btn = update.callback_query.data.split(' ')[0]
    if ' ' in update.callback_query.data:
        asset = update.callback_query.data.split(' ')[1]
    rynki = get_markets()
    pairs = rynki.keys()
    
    await update.callback_query.answer()

    '''
    print(list(pairs))

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=str(list(pairs))
    )
    '''
    
    if btn == 'buy':
        if asset + '-EUR' in pairs:
            buy_price = float(rynki[asset + '-EUR']['last_price']) * 1.04
        else:
            buy_price = float(rynki[asset + '-USDT']['last_price'])
            buy_price *= float(rynki['USDT-EUR']['last_price']) * 1.04
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'How much EUR do You want to spend? Type the number'
        )

        now = datetime.datetime.now()
        dead = now + datetime.timedelta(seconds=10)
        while datetime.datetime.now() < dead:
            number = get_quantity(update.effective_chat.id)

        received = number / buy_price
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'You will receive {received} {asset}'
        )
    elif btn == 'sell':
        print(asset)
        if asset + '-EUR' in pairs:
            sell_price = float(rynki[asset + '-EUR']['last_price']) * 0.96
        else:
            sell_price = float(rynki[asset + '-USDT']['last_price'])
            sell_price *= float(rynki['USDT-EUR']['last_price']) * 0.96
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'How much {asset} do You want to spend? Type the number'
        )

        now = datetime.datetime.now()
        dead = now + datetime.timedelta(seconds=10)
        while datetime.datetime.now() < dead:
            number = get_quantity(update.effective_chat.id)

        received = number * sell_price
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'You will receive {received} EUR'
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='unknown option selected'
        )
        return MENU
    return MENU

async def lang_func(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    
    if update.callback_query.data == 'en':
        await start_func(update, context)
    elif update.callback_query.data == 'it':
        await start_func(update, context)
    
    return

def get_quantity(sender_id):
    # print('get_quantity')
    parameters = {
        'offset': sender_id
    }
    responses = requests.get(TELE_API + TOKEN + get_updates, data=parameters)
    odpo = responses.json()
    if odpo['result']:
        wiado = odpo['result'][-1]['message']['text']
        for i in wiado:
            if i not in "1234567890.,":
                return 'invalid'
        if ',' in wiado:
            wiado.replace(',', '.')
        wiado = float(wiado)
        return wiado
    return


# when 'prices' button clcked
def read_msg(offset):
    parameters = {
        "offset": offset
    }

    responses = requests.get(TELE_API + TOKEN + get_updates, data = parameters)
    odpo = responses.json()
    if odpo['result']:
        osoba = odpo['result'][-1]['message']['chat']['id']
        wiado = odpo['result'][-1]['message']['text']
        send_msg(osoba, wiado)
        # return odpo['result'][-1]['update_id'] + 1
        return wiado.strip(' ').upper()
    return
    

def send_msg(osoba, wiado):
    rynki = get_markets()
    waluty = [i.split('-')[0] for i in rynki.keys()]
    if wiado.upper() in waluty:
        a, b = usdt_to_eur(wiado)
        out = f'Buy {wiado.upper()} for {a} EUR, \nsell {wiado.upper()} for {b} EUR'
    else:
        out = f'The selected asset ({wiado.upper()}) is unavailable. Select the currency You want to buy or sell\n\
            Type the ticker in order to check if it is available.'
    parameters2 = {
        "chat_id": osoba,
        "text": out
    }
    resp2 = requests.get(TELE_API + TOKEN + send_message, data = parameters2)
    return

def get_assets():
    resp3 = requests.get(KANGA_API + asset_list)
    assets = resp3.json()
    return assets

def get_markets():
    resp4 = requests.get(KANGA_API + market_tickers)
    rynki = resp4.json()
    return rynki

def usdt_to_pln(asset):
    asset = asset.upper()
    rynki = get_markets()
    pairs = rynki.keys()
    all = [i.split('-')[0] for i in pairs]
    if asset in all:
        to_pln = asset + '-PLN'
        to_usdt = asset + '-USDT'
        if to_pln in pairs:
            spot_price = float(rynki[to_pln]['last_price'])
        else:
            usd_spot_price = float(rynki[to_usdt]['last_price'])
            relation = float(rynki['USDT-PLN']['last_price'])
            spot_price = usd_spot_price * relation
        client_buys = spot_price * 1.04
        client_sells = spot_price * 0.96
        return client_buys, client_sells
    else:
        return -1.0, -1.0

def usdt_to_eur(asset):
    asset = asset.upper()
    rynki = get_markets()
    pairs = rynki.keys()
    all = [i.split('-')[0] for i in pairs]
    if asset in all:
        to_eur = asset + '-EUR'
        to_usdt = asset + '-USDT'
        if to_eur in pairs:
            spot_price = float(rynki[to_eur]['last_price'])
        else:
            usd_spot_price = float(rynki[to_usdt]['last_price'])
            relation = float(rynki['USDT-EUR']['last_price'])
            spot_price = usd_spot_price * relation
        client_buys = spot_price * 1.04
        client_sells = spot_price * 0.96
        return client_buys, client_sells
    else:
        return -1.0, -1.0

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    start_handler = CommandHandler('start', start_func, block=False)
    states = {MENU: [CallbackQueryHandler(button_func)],
              LANG: [CallbackQueryHandler(start_func)],
              ASSETS: [CallbackQueryHandler(button_func)],
              PRICES: [CallbackQueryHandler(buy_or_sell_func)]}

    fallbacks = [start_handler]
    conv_handler = ConversationHandler(
        entry_points=[start_handler],
        states=states,
        fallbacks=fallbacks,
        block=False
    )

    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(buy_or_sell_func))
    app.add_handler(CallbackQueryHandler(lang_func))
    # print(get_assets())
    app.run_polling()
    
    '''
    offset = 0
    while True:
        offset = read_msg(offset)'''
