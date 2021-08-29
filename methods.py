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
exportFilename = 'avitoExport.xml'

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

def downloadFile(url) -> str :

    re = requests.get(url)
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
            if row[1] == 'Категория 2' :
                continue
            else:
                xmlId = row[4]
                products[xmlId] = {
                    'id' : xmlId,
                    'title' : row[5],
                    'description' : getDescription(row[24], row[10]),
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
            for city in cities:
                newProduct = products[product].copy()
                cityId = city+products[product]['id']
                newProduct['cityId'] = cityId
                newProduct['address'] = cities[city]['address']

                resultArray[cityId] = newProduct
        
       # with open(pt.abspath('test.json'), 'w') as file :
        #    data = json.dumps(resultArray)
         #   file.write(data)

        root = et.Element('Ads', formatVersion="3", target="Avito.ru")

        for item in resultArray :

            ad = et.SubElement(root, 'Ad')

            productId  = et.SubElement(ad, 'Id')
            productId.text = resultArray[item]['cityId']
            avitoId = et.SubElement(ad, 'AvitoId')
            avitoId.text = resultArray[item]['cityId']

            #TODO: переделать на нормальные имена
            allowEmail1 = et.SubElement(ad, 'AllowEmail')
            allowEmail1.text = allowEmail

            managerName1 = et.SubElement(ad, 'ManagerName')
            managerName1.text = managerName

            contactPhone1 = et.SubElement(ad, 'ContactPhone')
            contactPhone1.text = contactPhone 

            address = et.SubElement(ad, 'Address')
            address.text = resultArray[item]['address']

            category1 = et.SubElement(ad, 'Category')
            category1.text = category

            goodsType1 = et.SubElement(ad, 'GoodsType')
            goodsType1.text = goodsType

            apparel1 = et.SubElement(ad, 'Apparel')
            apparel1.text = apparel

            size1 = et.SubElement(ad, 'Size')
            size1.text = size

            condition1 = et.SubElement(ad, 'Condition')
            condition1.text = condition

            title = et.SubElement(ad, 'Title')
            title.text = resultArray[item]['title']

            description = et.SubElement(ad, 'Description')
            description.text = resultArray[item]['description']

            price = et.SubElement(ad, 'Price')
            price.text = str(resultArray[item]['price'])

            images = et.SubElement(ad, 'Images')
            imageList = resultArray[item]['images']
            for image in imageList :
                tag = et.SubElement(images, 'Image' , url=image)

        tree = et.ElementTree(root)
        tree.write(exportFilename, pretty_print=True, xml_declaration=True,   encoding="utf-8")


createAvitoFeed()
            