from model import Contacts
import connection_to_mongo

import pika

#connect to RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

#declaring the queue for sending messages
channel.queue_declare(queue='email_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

#function to simulate sending email messages
def send_email(contact):
    return f"For {contact} send email"


#function for processing messages from the RabbitMQ queue and simulating sending them to contacts
def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contacts.objects(id=contact_id).first()
    if contact:
        print(send_email(contact_id))
        contact.update(done=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)

#getting messages from a RabbitMQ queue
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='email_queue', on_message_callback=callback)

if __name__ == '__main__':
    channel.start_consuming()