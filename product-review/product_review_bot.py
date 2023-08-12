import telebot
import time
import requests
from bs4 import BeautifulSoup
from telebot import types
bot=telebot.TeleBot('', threaded=False)
@bot.message_handler(commands=["start"])
def start(message, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Посмотреть рейтинг товара")
    item2 = types.KeyboardButton("О нас")
    markup.add(item1,item2)
    bot.send_photo(message.chat.id,'https://postimg.cc/d7r8xfVR')
    bot.send_message(message.chat.id, 'Здравствуйте, '+message.from_user.first_name+'!\n Я - бот-поисковик, который поможет вам получить информацию о названии товара, его среднем рейтинге и ссылке на коллекцию отзывов о нём. Если вы готовы ли вы получить её, выберите нужную вам кнопку.', reply_markup=markup)
@bot.message_handler(content_types=['text'])
def search(message):
 if message.chat.type == 'private':
   if message.text == 'Посмотреть рейтинг товара':
        time.sleep(0.5)
        bot.send_message(message.chat.id, 'Опишите товар, который вам нужно проверить')
   else:
       if message.text!='О нас':
        time.sleep(0.5)
        bot.send_message(message.chat.id,'Обрабатываем ваш запрос...')
        search = message.text
        url = (f'https://irecommend.ru/srch?query={requests.utils.quote(search)}')
        r = requests.get(url)
        link = BeautifulSoup(r.text, 'lxml')
        for div in link.findAll('div', attrs={'class': 'ProductTizer'}):
            name=div.find('div', class_='title').text
            rating=div.find('span', class_='average-rating').text
            link=div.find('a', class_='reviewsLink')['href']
            image=div.find('div',class_='image')
            image=image.find('img',class_='lazy lazy-loader')['data-original']
            text = (f'Наименование: {name}\nРейтинг {rating}\nСсылка: https://irecommend.ru{link}')
            bot.send_photo(message.chat.id, f'{image}', caption=text)
        bot.send_message(message.chat.id,'Желаете ещё что-нибудь проверить?')
       else:
           if message.text == 'О нас':
               bot.send_photo(message.chat.id, 'https://postimg.cc/HJ9D6cpz')
               bot.send_message(message.chat.id, 'Мы - команда, состоящая всего из двух человек.\nНо разработавшая этого бота своими усилиями в рамках образовательной программы "Сириуса". Немного о нас:\nСофья Дворцова - директор по дизайну, разработчик визуальной части. Призёр Всероссийского конкурса "Большая перемена", призёр проектной школы "Креативные индустрии" по направлению "Разработка видеоигр, виртуальной и дополненной реальности".\nЕгор Чуланов - директор по информационным технологиям. Участник интенсивов "Медиажурналистика-PRO", "Таланты - 2030".\n\nМы надеемся, что наш бот поможет вам в удовлетворении ваших потребностей и надеемся на дальнейшее его использование вами.')
bot.infinity_polling()
