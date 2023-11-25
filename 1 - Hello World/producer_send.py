import pika

connection_params = pika.ConnectionParameters('localhost')
with pika.BlockingConnection(connection_params) as connection:
    channel = connection.channel()
    # we need to make sure the recipient queue exists. 
    # If we send a message to non-existing location, RabbitMQ will just drop the message
    channel.queue_declare(queue='hello') # Does this return something? 
    # Messages needs to go through an exchange. 
    channel.basic_publish(exchange='', # default exchange 
                        routing_key='hello', # The queue name
                        body='Hello World!')
    print(" [x1] Sent 'Hello World!'")