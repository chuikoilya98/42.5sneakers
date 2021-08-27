import requests
import json
import os.path as pt
from lxml import etree as et
import csv

import re


string = 'https://bizoutmax.ru/image/data/products/25060/krossovki-adidas-ultra-boost-1.jpg'



def getr(string) :
    links = []
    while string.find(',') != -1 :
        k = string.find(',')

        link = string[:k]

        links.append(link)
        string = string[k+1:]
    links.append(string)

    return links

getr(string)