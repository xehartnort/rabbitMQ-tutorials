import pika, sys, os

def main():
    connection_params = pika.ConnectionParameters(host='localhost')
    with pika.BlockingConnection(connection_params) as connection:
        channel = connection.channel()
        # Recomendable to do this always, even is the queue is already declared
        channel.queue_declare(queue='hello')

        def callback(ch, method, properties, body):
            # print(f" [x] Received {body}, properties: {properties}, method: {method}, ch:{ch}")
            print(f" [x] Received {body}")

        channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming() # This proces an endless loop

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)