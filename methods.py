import requests
import json
import os.path as pt
from lxml import etree as et
import csv
import re

credFilename = 'credentials.json'
csvFilename = 'products.csv'
citiesFilename = 'cities.json'
descriptionFilename = 'description.txt'
fileTemporaryUrl = 'https://cloudparser.ru/export/82553-2-913442777'

#avito globals
size = '41'
allowEmail = 'Да'
managerName = 'Иван Алексеев'
contactPhone = '89995862639'
category = 'Одежда, обувь, аксессуары'
goodsType = 'Мужская одежда'
apparel = 'Обувь'
condition = 'Новое'

def getCredentials() -> dict:

    with open(pt.abspath(credFilename), 'r',encoding='utf-8') as file :
        data = json.load(file)
        return data

def sendMessage( text:str) -> None :

    creds = getCredentials()
    chatIds = creds['chatId']
    token = creds['token']

    for chat in chatIds :
        url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat}&text={text}'
        message = requests.get(url)

def downloadFile() -> str :

    re = requests.get(fileTemporaryUrl)
    re.encoding = 'utf-8'

    if re.status_code == 200 :
        with open(pt.abspath(csvFilename), 'wb') as file :
            file.write(re.content)
        result = 'Выгрузка успешно загружена'
    else :
        result = 'Произошла ошибка при загрузке файла'

    return result

def getCitiesInfo() -> dict :
        with open(citiesFilename, 'r', encoding='utf-8') as file :
            data = json.load(file)
        return data

def getDescription(sizes:str,description:str) -> str :

    descriptionText = ''
    with open(pt.abspath(descriptionFilename), 'r', encoding='utf-8') as file :
        for line in file :
            descriptionText += line

    text = description + '\n'
    text += 'РАЗМЕРЫ' + '\n'
    text += sizes + '\n'
    text += descriptionText

    return text

def getImages(string:str) -> list:
    links = []
    while string.find(',') != -1 :
        k = string.find(',')

        link = string[:k]

        links.append(link)
        string = string[k+1:]
    links.append(string)

    return links

def createAvitoFeed() -> str :

    cities = getCitiesInfo()

    with open(pt.abspath(csvFilename), 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        products = {}
        resultArray = {}

        for row in reader :
            if row[0] == '"Категория 1"' :
                continue
            else:
                xmlId = row[4]
                products[xmlId] = {
                    'title' : row[5],
                    #'description' : getDescription(row[24], row[10]),
                    'size' : size,
                    'price' : row[6],
                    'images' : getImages(row[11]),
                    'allowEmail' : allowEmail,
                    'managerName' : managerName,
                    'contactPhone' : contactPhone,
                    'category' : category,
                    'goodsType' : goodsType,
                    'apparel' : apparel,
                    'condition' : condition
                }

        for product in products :
            for city in cities :
                cityId = city + product
                products[product]['cityId'] == cityId

                print(products[product])

            