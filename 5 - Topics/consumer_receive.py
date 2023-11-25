import pika
import sys

def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

connection_params = pika.ConnectionParameters(host='localhost')

with pika.BlockingConnection(connection_params) as connection:

    channel = connection.channel()
    # Declare exchange with anonymous and exclusive queue
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
    result = channel.queue_declare(queue='', exclusive=True) # Exclusiva a esta conexión
    queue_name = result.method.queue

    for binding_key in binding_keys:
        # Crea un bind para cada severidad, se genera un nombre de queue en cada bind
        channel.queue_bind(
            exchange='topic_logs', queue=queue_name, routing_key=binding_key)

    print(' [*] Waiting for logs. To exit press CTRL+C')


    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()