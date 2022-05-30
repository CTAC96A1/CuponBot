from telegram import Update
from telegram.ext import Updater
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from bs4 import BeautifulSoup as BS
import requests

button_KFC = 'KFC'
button_BKING = 'Бургер Кинг'
base_url = 'https://www.kfc.ru/coupons'
burking_url = 'https://burgerk.club'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)' 
    'Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.243 (Edition Yx)',
    'accept' : '*/*'
}
HEADERSBUR = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.243 (Edition Yx)',
    'accept' : '*/*'
}

def parser(url):
    session = requests.Session()
    responce = session.get(url, headers=HEADERS)
    soup = BS(responce.content, 'html.parser')
    items = soup.find_all('div', class_= '_2NyuN9wIxb _2863BpiS1v mr-32 mb-64')

    coupons_str = ' '
    for names in items:
        header = names.find('div', class_= '_3POebZQSBG t-md c-description mt-16 pl-24 pr-24 condensed').text
        coup = names.find('div', class_='_2pr76I4WPm').text
        if (names.find('span', class_='_1trEHSCHMh condensed c-primary bold')!= None):
            cost = names.find('span', class_='_1trEHSCHMh condensed c-primary bold').text
        if cost != None:
            coupons_str += coup+ " " + header +"\n"+ cost + " ₽\n\n"
        else:
            coupons_str += coup + " " + header + " "
    return coupons_str

def parserBK(url):
    session = requests.Session()
    responce = session.get(url, headers=HEADERSBUR)
    soup = BS(responce.content, 'html.parser')
    items = soup.find_all('div', class_='coupon')

    coupons_str = ' '
    for names in items:
        header = names.find('div', class_='coun').text
        structure = names.find('div', class_='cous').text
        cost = names.find('div', class_='couc').text

        coupons_str += header+" В наборе:"+structure+" "+ cost+"\n\n"
    return  coupons_str



def button_KFC_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=parser(url=base_url),
    )

def button_BKING_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=parserBK(url=burking_url),
    )




def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text == button_KFC:
        return button_KFC_handler(update=update, context=context)
    elif text == button_BKING:
        return button_BKING_handler(update=update, context=context)

    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_KFC)
            ],
            [
                KeyboardButton(text=button_BKING)
            ],
        ],
        resize_keyboard= True,
    )

    update.message.reply_text(
        text='Выберите закусочную, для которой хотите посмотреть купоны(в Макдональдсе нет купонов)',
        reply_markup=reply_markup,
    )


def main():
    print('Start')
    updater = Updater(
        token='1799625335:AAFiHfiLCF2RxeQC2Yf3uQWzgznWqrmZ97w',
        use_context=True,
    )
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()



