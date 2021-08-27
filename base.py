from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/cloudparser', methods = ['GET'])
def hook():
    data = request.args.get('key1')
    print(data)
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0')