
import pika
import json

params = pika.URLParameters(
    'amqps://qwsrvkqg:4s2YX68Qo_XGjW5zIl-2DHYXEAL5oYQR@hog.rmq5.cloudamqp.com/qwsrvkqg')
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='reviews',
                          body=body, properties=properties)
