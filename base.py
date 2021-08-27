from flask import Flask
from flask import request
from methods import sendMessage

app = Flask(__name__)

@app.route('/cloudparser', methods = ['GET'])
def hook():
    
    url = request.args.get('url')
    productsCount = request.args.get('productsCount')

    sendMessage(f'Выгрузка товаров ВК завершена, сегодня активно {productsCount} товаров. Стартуем сбор данных для Яндекс Объявлений')

    return url

if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    app.run(debug=True)