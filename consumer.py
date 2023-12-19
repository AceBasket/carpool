#i want this to recieve information from the producer, which is information from a database with reviews
#using pika
import json
import pika

params = pika.URLParameters('amqps://qwsrvkqg:4s2YX68Qo_XGjW5zIl-2DHYXEAL5oYQR@hog.rmq5.cloudamqp.com/qwsrvkqg')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='reviews')


def callback(ch, method, properties, body):
    print('Received in reviews')
    print(body)
    data = json.loads(body)
    print(data)
    if properties.content_type == 'review_created':
        id=data['id']
        reviewer=data['reviewer']
        reviewee=data['reviewee']
        trip=data['trip']
        print('Review created')
    elif properties.content_type == 'review_updated':
        print('Review updated')
    elif properties.content_type == 'review_deleted':
        print('Review deleted')


channel.basic_consume(queue='reviews', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

#try:
channel.start_consuming()
#except Exception as e:
#    print(f"An error occurred: {e}")

channel.close()
