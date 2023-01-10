from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import math
import time
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import os


def get_offer_info(country, post, location):
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    list_offers = []
    driver.get(f'https://{country}.indeed.com/jobs?q={post}&l={location}&fromage=1')
    offers = BeautifulSoup(driver.find_element(By.XPATH, "//div[@class='jobsearch-LeftPane']").get_attribute('innerHTML'), "html.parser")
    offers_number = offers.find(class_='jobsearch-JobCountAndSortPane-jobCount').text
    if '\xa0' in offers_number:
        offers_number = int(offers_number.split('\xa0')[0])
    else:
        offers_number = int(offers_number.split(' ')[0])
    pages_number = math.ceil(offers_number/ 15)

    for i in range (1, pages_number+1):
        x = i*10-10
        driver.get(f'https://{country}.indeed.com/jobs?q={post}&l={location}&fromage=1&start={x}')
        offers = BeautifulSoup(driver.find_element(By.XPATH, "//div[@class='jobsearch-LeftPane']").get_attribute('innerHTML'),"html.parser")
        for offer in offers.find_all('h2')[:-1]:
            if f'https://{country}.indeed.com' not in offer.find('a').get("href"):
                list_offers.append(f'https://{country}.indeed.com' + offer.find('a').get("href"))
            else:
                list_offers.append(offer.find('a').get("href"))
    return offers_number, list_offers



bot = Bot(token = os.getenv('token2'))
dp = Dispatcher(bot)

print('Starting a bot...')

button1 = KeyboardButton('HELP')
keyboard1 = ReplyKeyboardMarkup(resize_keyboard = True).add(button1)


@dp.message_handler(commands= ['start'])
async def choose_button(message: types.Message):
    await message.reply('This bot shows the latest vacancies posted in the last day \nTo start the search, you must enter the search parameters in the format \n country abbreviation vacancy name (separated by + if the vacancy consists of two words) city/country name \nExample \nfr data+analyst Paris', reply_markup = keyboard1)



@dp.message_handler()
async def answer_job(message: types.Message):
    if message.text == 'HELP':
        await message.reply("Source of info: indeed \nPeriod of the publication : 24 h \nList of countries abbreviation https://developer.indeed.com/docs/publisher-jobs/countries \nMore examples of correct input \ncn data+scientist Shanghai \nde data+analyst Berlin \nau project+manager Sydney \n \nThis bot can not parse offers from US")
    else:
        try:
            list_params = message.text.split()
            offers_number, list_offers = get_offer_info(list_params[0], list_params[1], list_params[2])
            await message.reply(offers_number)
            for elem in list_offers:
                await message.reply(elem)

        except:
            await message.reply(f"Wrong format start again /start")




executor.start_polling(dp)