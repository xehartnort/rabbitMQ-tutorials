import pika
import time

connection_params = pika.ConnectionParameters(host='localhost')
queue_name = 'task_queue'
with pika.BlockingConnection(connection_params) as connection:
    channel = connection.channel()
    # Recomendable to do this always, even is the queue is already declared
    # channel.queue_declare(queue='hello') # si la quiero hacer permanente, tendré que cambiarle el nombre
    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}, {type(body)}")
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_qos(prefetch_count=1) # Los mensajes se envían a los consumidores libres, si estos ya tienen un mensaje
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming() # This proces an endless loop
