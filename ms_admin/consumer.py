import json
import os
import pika
import django


def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ms_admin.settings')
    django.setup()


setup_django()

params = pika.URLParameters(
    'amqps://gampxowk:AAz395sATutJhZizqPMAS6i0ZWH332Zh@puffin.rmq2.cloudamqp.com/gampxowk'
)
connection = pika.BlockingConnection(parameters=params)
channel = connection.channel()
channel.queue_declare(queue='admin')


def callback(_channel, method, properties, body):
    from products.models import Product

    if properties.content_type == 'product_like':
        pk = json.loads(body)
        product = Product.objects.get(id=pk)
        product.likes += 1
        product.save()


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
channel.close()
