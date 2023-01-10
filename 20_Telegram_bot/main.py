from selenium import webdriver
from selenium.webdriver.common.by import By
import math
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import os

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)


def get_number_of_offers():
    driver.get('https://fr.indeed.com/jobs?q=data+analyst&l=Occitanie&fromage=1')
    offers = BeautifulSoup(
        driver.find_element(By.XPATH, "//div[@class='jobsearch-LeftPane']").get_attribute('innerHTML'), "html.parser")
    offers_number = int(offers.find(class_='jobsearch-JobCountAndSortPane-jobCount').text.split('\xa0')[0])
    return offers_number


pages_number_Occitanie = math.ceil(get_number_of_offers() / 15)


def get_offer_info():
    list_offers = []
    for i in range(1, pages_number_Occitanie + 1):
        x = i * 10 - 10
        driver.get(f'https://fr.indeed.com/jobs?q=data+analyst&l=Occitanie&fromage=1&start={x}')
        offers = BeautifulSoup(
            driver.find_element(By.XPATH, "//div[@class='jobsearch-LeftPane']").get_attribute('innerHTML'),
            "html.parser")
        for offer in offers.find_all('h2')[:-1]:
            if 'https://fr.indeed.com' not in offer.find('a').get("href"):
                list_offers.append('https://fr.indeed.com' + offer.find('a').get("href"))
            else:
                list_offers.append(offer.find('a').get("href"))
    return list_offers


def get_number_remote_offers():
    driver.get('https://fr.indeed.com/jobs?q=data+analyst&l=France&sc=0kf%3Aattr%28DSQF7%29%3B&fromage=1')
    offers = BeautifulSoup(
        driver.find_element(By.XPATH, "//div[@class='jobsearch-LeftPane']").get_attribute('innerHTML'), "html.parser")
    offers_number = int(offers.find(class_='jobsearch-JobCountAndSortPane-jobCount').text.split('\xa0')[0])
    return offers_number


pages_number_remote_offers = math.ceil(get_number_remote_offers() / 15)


def get_remote_offer_info():
    list_offers = []
    for i in range(1, pages_number_remote_offers + 1):
        x = i * 10 - 10
        driver.get(
            f'https://fr.indeed.com/jobs?q=data+analyst&l=France&sc=0kf%3Aattr%28DSQF7%29%3B&fromage=1&start={x}')
        offers = BeautifulSoup(
            driver.find_element(By.XPATH, "//div[@class='jobsearch-LeftPane']").get_attribute('innerHTML'),
            "html.parser")
        for offer in offers.find_all('h2')[:-1]:
            if 'https://fr.indeed.com' not in offer.find('a').get("href"):
                list_offers.append('https://fr.indeed.com' + offer.find('a').get("href"))
            else:
                list_offers.append(offer.find('a').get("href"))
    return list_offers


bot = Bot(token=os.getenv('token1'))
dp = Dispatcher(bot)

print('Starting a bot...')

button1 = KeyboardButton('Show offers in Occitanie')
button2 = KeyboardButton('Show remote offers in France')
button3 = KeyboardButton('Total offers')


keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button1, button2, button3)


@dp.message_handler(commands=['start'])
async def choose_button(message: types.Message):
    await message.reply('Hello, good luck in your search! I can show you remote offers in France and on site offers in Occitanie for the last 24 hours', reply_markup=keyboard1)



@dp.message_handler()
async def answer_job(message: types.Message):
    if message.text == 'Show offers in Occitanie':
        for elem in get_offer_info():
            await message.reply(elem)
    elif message.text == 'Show remote offers in France':
        for elem in get_remote_offer_info():
            await message.reply(elem)
    elif message.text == "Total offers":
        await message.reply('For the last 24 hours total number of interesting offers: ' + str(get_number_of_offers() + get_number_remote_offers()))
    else:
        await message.reply(f"I don't know this command, please type /start")


executor.start_polling(dp)
