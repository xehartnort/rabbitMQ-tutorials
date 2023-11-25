import pika
import sys

def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

connection_params = pika.ConnectionParameters(host='localhost')

with pika.BlockingConnection(connection_params) as connection:

    channel = connection.channel()
    # Declare exchange with anonymous and exclusive queue
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
    result = channel.queue_declare(queue='', exclusive=True) # Exclusiva a esta conexión
    queue_name = result.method.queue

    for severity in severities:
        # Crea un bind para cada severidad, se genera un nombre de queue en cada bind
        channel.queue_bind(
            exchange='direct_logs', queue=queue_name, routing_key=severity)

    print(' [*] Waiting for logs. To exit press CTRL+C')


    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()