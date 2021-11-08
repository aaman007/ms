import random
from dataclasses import dataclass

import requests
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from producer import publish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://aaman007:password@db/main'
CORS(app)

db = SQLAlchemy(app)


@dataclass
class Product(db.Model):
    id: int
    name: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(255))
    image = db.Column(db.String(200))


@dataclass
class ProductUser(db.Model):
    id: int
    user_id: int
    product_id: int

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:pk>/like', methods=['POST'])
def like(pk):
    res = requests.get('http://host.docker.internal:8080/products/user/')
    user_id = res.json()['id']
    print(user_id)
    # user_id = random.randint(1, 100)
    try:
        product = ProductUser(user_id=user_id, product_id=pk)
        db.session.add(product)

        publish('product_like', pk)
    except:
        abort(400, 'Already liked')

    return jsonify({
        'status': 'success'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
