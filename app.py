from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017")
db = client.pyladies  # database - pyladies - collection - books

@app.route('/book', methods=['GET'])
def get_all_books():
    book = db.book
    output = []
    for b in book.find():
        output.append({'name': b['name'], 'pages': b['pages']})
    return jsonify({'result': output})


@app.route('/add', methods=['POST'])
def add_books():
    _json = request.json
    _name = _json['name']
    _pages = _json['pages']
    if _name and _pages:
        id = db.book.insert({'name': _name, 'pages': _pages})
        resp = jsonify('Book added!')
        resp.status_code = 200
        return resp
    else:
        return False


@app.route('/search/<name>')
def book(name):
    one_book = db.book.find_one({'name': name})
    resp = dumps(one_book)
    return resp


if __name__ == '__main__':
    app.run(debug=True)
