# Sending_messages_with_RabbitMQ
This project has two scripts producer.py and consumer.py

When you run the producer.py script, it generates a certain number of fake contacts and writes them to the database. Then it puts a message in the RabbitMQ queues that contains the ObjectID of the created contact, and so on for all generated contacts.

The consumer.py script receives a message from the RabbitMQ queue, processes it, and simulates sending the message with a stub function.

After the message is sent, the boolean field for the contact changes to True. The script runs constantly waiting for incoming messages from RabbitMQ.
