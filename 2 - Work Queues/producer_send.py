import pika
import sys

connection_params = pika.ConnectionParameters('localhost')
queue_name = 'task_queue'
with pika.BlockingConnection(connection_params) as connection:
    channel = connection.channel()
    # we need to make sure the recipient queue exists. 
    # If we send a message to non-existing location, RabbitMQ will just drop the message
    channel.queue_declare(queue=queue_name, durable=True) # Does this return something? 
    # Messages needs to go through an exchange. 
    message = ' '.join(sys.argv[1:]) or "Hello World!"
    # Persistent queue with durable=True and sending persisting messages, both are needed
    # Still messages are not synced in disk, so they might be wrote to cache instead, beware
    channel.basic_publish(exchange='',
                        routing_key=queue_name,
                        body=message,
                        properties=pika.BasicProperties(
                            delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
                        )
                        )
    print(f" [x] Sent {message}")