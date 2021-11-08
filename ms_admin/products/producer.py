import json
import pika

params = pika.URLParameters(
    'amqps://gampxowk:AAz395sATutJhZizqPMAS6i0ZWH332Zh@puffin.rmq2.cloudamqp.com/gampxowk'
)
connection = pika.BlockingConnection(parameters=params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
