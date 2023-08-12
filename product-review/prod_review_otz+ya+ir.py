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
    item3=types.KeyboardButton('О боте')
    markup.add(item1,item2,item3)
    bot.send_photo(message.chat.id,'https://postimg.cc/d7r8xfVR', caption='Здравствуйте, '+message.from_user.first_name+'!\n Я - бот-поисковик, который поможет вам получить информацию о названии товара, его среднем рейтинге и ссылке на коллекцию отзывов о нём. Если вы готовы ли вы получить её, выберите нужную вам кнопку.', reply_markup=markup)
@bot.message_handler(content_types=['text'])
def buttons(message):
 if message.chat.type == 'private':
   if message.text == 'Посмотреть рейтинг товара':
       sites = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
       site1 = types.InlineKeyboardButton(text='iRecommend')
       site2 = types.InlineKeyboardButton(text='Otzovik (Скоро)')
       site3 = types.InlineKeyboardButton(text='Яндекс.Маркет (Скоро)')
       sites.add(site1, site2, site3)
       time.sleep(0.5)
       mesg=bot.send_message(message.chat.id, 'Выберите, с какого сайта мы будем искать отзывы',reply_markup=sites)
       bot.register_next_step_handler(mesg, welcome)
   elif message.text == 'О нас':
        bot.send_photo(message.chat.id, 'https://postimg.cc/9RtNvYpH', caption='Немного обо мне:\nЯ, Софья Дворцова - директор по дизайну, разработчик визуальной части, а также главный кодер.\n- Призёр Всероссийского конкурса "Большая перемена"\n- Призёр проектной школы "Креативные индустрии" по направлению "Разработка видеоигр, виртуальной и дополненной реальности"\n- Участник Инженерно-технической и гуманитарной смены от ХМАО-Югры в Образовательном центре "Сириус", Сочи по направлению "Информационные технологии".\n\nДо жути люблю путешествовать и посещать различные мероприятия: стала участником фестиваля Детства и юности на ВДНХ в городе Москве, июнь 2022 года. В апреле 2023 я полечу в Санкт-Петербург в рамках программы "Больше, чем путешествие", а в июле мне предстоит визит в Карелию.\n\nЯ надеюсь, что мой бот поможет вам в удовлетворении ваших потребностей и надеюсь на дальнейшее его использование вами.')
   elif message.text=='О боте':
        bot.send_photo(message.chat.id, 'https://postimg.cc/t7sqG16n' , caption='SiteReviewBot - бот, созданный в рамках Инженерно-технической и гуманитарной смены от Ханты-Мансийского Автономного округа - Югры в образовательном центре "Сириус", Сочи. Бот изначально создавался в качестве забавы и очередного проекта, который я, в конце-концов, заброшу. Но все-таки я пришла к решению: буду постепенно развивать бота, чтобы он действительно помог людям.\n\nВ основе работы данного Telegram-бота - код на языке Python. Бот берёт код со страницы поиска заданного вами товара с помощью библиотеки Requests, парсит (собирает) данные о самих продуктах с помощью BeautifulSoup и выдаёт вам то, что нужно.\nНа данный момент в наличии имеется только один сайт отзывов, с которого бот берёт данные - iRecommend, так как Отзовик и Яндекс.Маркет не пропускают ботов. Но я очень стараюсь, чтобы решить данную проблему. Удачного тебе дня, и спасибо за прочтение поста! :)')
@bot.message_handler(content_types=['text'])
def welcome(message):
    if message.chat.type == 'private':
        if message.text=='iRecommend':
            msg=bot.send_message(message.chat.id, 'Опишите товар, который вам нужно проверить')
            bot.register_next_step_handler(msg,irsearch)
        elif message.text=='Otzovik':
            msg = bot.send_message(message.chat.id, 'Опишите товар, который вам нужно проверить')
            bot.register_next_step_handler(msg, otzsearch)
        elif message.text=='Яндекс.Маркет':
            msg=bot.send_message(message.chat.id, 'Опишите товар, который вам нужно проверить')
            bot.register_next_step_handler(msg,yasearch)
def irsearch(message):
    time.sleep(0.5)
    bot.send_message(message.chat.id, 'Обрабатываем ваш запрос...')
    search = message.text
    url = (f'https://irecommend.ru/srch?query={requests.utils.quote(search)}')
    r = requests.get(url)
    link = BeautifulSoup(r.text, 'lxml')
    for div in link.findAll('div', attrs={'class': 'ProductTizer'}):
        name = div.find('div', class_='title').text
        rating = div.find('span', class_='average-rating').text
        link = div.find('a', class_='reviewsLink')['href']
        image = div.find('div', class_='image')
        image = image.find('img', class_='lazy lazy-loader')['data-original']
        text = (f'Наименование: {name}\nРейтинг {rating}\nСсылка: https://irecommend.ru{link}')
        bot.send_photo(message.chat.id, f'{image}', caption=text)
    bot.send_message(message.chat.id, 'Желаете ещё что-нибудь проверить?')
def otzsearch(message):
    time.sleep(0.5)
    bot.send_message(message.chat.id, 'Обрабатываем ваш запрос...')
    search=message.text
    url=(f'https://otzovik.com/?search_text={requests.utils.quote(search)}&x=0&y=0')
    r=requests.get(url)
    print(r)
    link=BeautifulSoup(r.text,'lxml')
    for div in link.findAll('tr',class_='item sortable'):
        name=div.find('a',class_='product-name').text
        rating=div.find('div',class_='product-rating tooltip-left hover-brace').text
        link=div.find('a',class_='reviews-counter')['href']
        image=div.find('div',class_='product-photo has-photo')['data-orig']
        text=(f'Наименование:{name}\nРейтинг {rating}\nСсылка: https://otzovik.com{link}')
        bot.send_photo(message.chat.id,f'{image}',caption=text)
    bot.send_message(message.chat.id, 'Желаете ещё что-нибудь проверить?')
def yasearch(message):
    time.sleep(0.5)
    bot.send_message(message.chat.id,'Обрабатываем ваш запрос...')
    search=message.text
    url=(f'https://market.yandex.ru/catalog/83829/list?srnum=1172&was_redir=1&rt=9&rs=eJwzEglgrGLlWHzlMfssRo6LzRebLvZd2AwAVoAJrA%2C%2C&suggest_text={requests.utils.quote(search)}&hid=16312867&allowCollapsing=1&local-offers-first=0')
bot.infinity_polling()
