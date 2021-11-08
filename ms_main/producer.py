import pika
import json

params = pika.URLParameters(
    'amqps://gampxowk:AAz395sATutJhZizqPMAS6i0ZWH332Zh@puffin.rmq2.cloudamqp.com/gampxowk'
)
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
