
import pika
import json

params = pika.URLParameters(
    'amqps://qwsrvkqg:4s2YX68Qo_XGjW5zIl-2DHYXEAL5oYQR@hog.rmq5.cloudamqp.com/qwsrvkqg')
connection = pika.BlockingConnection(params)
channel = connection.channel()

# send the data with identifying fields for reviewer, reviewee and trip


def publish(method, body):
    # reviews=fetch_reviews()
    # reviews_to_publish=[obj.to_json() for obj in reviews]
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='reviews',
                          body=body, properties=properties)
    if method == 'trip_deleted':
        print('deleted trip id '+str(body)+' sent')
