import pika
import sys

connection_params = pika.ConnectionParameters('localhost')
with pika.BlockingConnection(connection_params) as connection:
    channel = connection.channel()
    message = ' '.join(sys.argv[1:]) or "Hello World!"
    # No declaramos una cola porque vamos a usar porque será por defecto y además usamos fanout
    # Instead of directly connecting to a queue, it is common to use an connect to an exchange
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    # As we are using fanout, we do not need to specifcy a routing_key (a queue name)
    message = ' '.join(sys.argv[1:]) or "info: Hello World!"
    channel.basic_publish(exchange='logs', routing_key='', body=message)

    print(f" [x] Sent {message}")