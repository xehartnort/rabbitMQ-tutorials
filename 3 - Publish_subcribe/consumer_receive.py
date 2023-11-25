import pika
import time

connection_params = pika.ConnectionParameters(host='localhost')
with pika.BlockingConnection(connection_params) as connection:
    channel = connection.channel()

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}, {type(body)}")
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    # Declaramos un exchange
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    # Declaramos una cola
    result = channel.queue_declare(queue='', exclusive=True) # disposable queue
    # Conectamos la cola con el exchange
    # Gather queue name, given that its name is randomly asigned
    queue_name = result.method.queue
    channel.queue_bind(exchange='logs', queue=queue_name) # relacionar el exchange con la cola, así están conectados
    # Un exchange se puede conectar a múltiples colas
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming() # This proces an endless loop
