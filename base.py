from flask import Flask
from flask import request
from flask import send_file, send_from_directory
from methods import sendMessage
import os.path as pt
import os
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index() :
    return 'hello world'

@app.route('/products', methods=['GET'])
def getDocs():

    if request.method == 'GET' and request.args.get('source') == 'oyandex':
        path = os.getcwd()
        return send_from_directory(path, 'avitoExport.xml')
    else :
        return 'Eternal Error'

@app.route('/cloudparser', methods = ['GET'])
def hook():
    
    url = request.args.get('url')
    productsCount = request.args.get('productsCount')

    sendMessage(f'Выгрузка товаров ВК завершена, сегодня активно {productsCount} товаров. Стартуем сбор данных для Яндекс Объявлений. Ссылка на товар - {url}')

    return 'success'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    #app.run(debug=True)