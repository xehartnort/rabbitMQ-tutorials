#!/usr/bin/env python
import pika
import sys

connection_params = pika.ConnectionParameters(host='localhost')
with pika.BlockingConnection(connection_params) as connection:

    channel = connection.channel()

    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

    severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
    message = ' '.join(sys.argv[2:]) or 'Hello World!'

    channel.basic_publish(
        exchange='direct_logs', 
        routing_key=severity, 
        body=message
    )
    print(f" [x] Sent {severity}:{message}")
