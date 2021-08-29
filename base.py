from flask import Flask
from flask import request
from flask import send_file
from methods import sendMessage
import os.path as pt
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    info = pt.abspath('products.csv')

    return info

@app.route('/cloudparser', methods = ['GET'])
def hook():
    
    url = request.args.get('url')
    productsCount = request.args.get('productsCount')

    sendMessage(f'Выгрузка товаров ВК завершена, сегодня активно {productsCount} товаров. Стартуем сбор данных для Яндекс Объявлений. Ссылка на товар - {url}')

    return 'success'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    #app.run(debug=True)