import json

import pika

from main import Product, db

params = pika.URLParameters(
    'amqps://gampxowk:AAz395sATutJhZizqPMAS6i0ZWH332Zh@puffin.rmq2.cloudamqp.com/gampxowk'
)
connection = pika.BlockingConnection(parameters=params)
channel = connection.channel()
channel.queue_declare(queue='main')


def callback(_channel, method, properties, body):
    data = json.loads(body)

    if properties.content_type == 'product_create':
        product = Product(id=data['id'], name=data['name'], image=data['image'])
        db.session.add(product)
        db.session.commit()
    elif properties.content_type == 'product_update':
        product = Product.query.get(data['id'])
        product.name = data['name']
        product.image = data['image']
        db.session.commit()
    elif properties.content_type == 'product_delete':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
channel.close()
