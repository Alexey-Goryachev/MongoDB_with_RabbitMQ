from model import Contacts
import connection_to_mongo

import pika

from faker import Faker

fake = Faker('uk-UA')

#connect to RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

#declaring the exchange and queues for sending messages
channel.exchange_declare(exchange='contacts', exchange_type='direct')
channel.queue_declare(queue='email_queue', durable=True)
channel.queue_declare(queue='sms_queue', durable=True)
channel.queue_bind(exchange='contacts', queue='email_queue')
channel.queue_bind(exchange='contacts', queue='sms_queue')


#function to create and write contacts to the MongoDB, and after the messages are placed in the RabbitMQ queue for each created contact
def main():
    for _ in range(5):
        contact = Contacts(fullname=fake.name(), email=fake.email(), number_phone=fake.phone_number(), address=fake.address(), preferred_method=fake.random_element(elements=('email', 'sms'))).save()
        if contact.preferred_method == 'email':
            routing_key = 'email_queue'
            channel.basic_publish(exchange='contacts', 
                                routing_key=routing_key,
                                body=str(contact.id).encode(),
                                properties=pika.BasicProperties(
                                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
            
            print(f"Sent email {contact}")
        else:
            routing_key = 'sms_queue'
            channel.basic_publish(exchange='contacts', 
                                routing_key=routing_key,
                                body=str(contact.id).encode(),
                                properties=pika.BasicProperties(
                                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
            
            print(f"Sent sms {contact}")



if __name__ == '__main__':
    main()
