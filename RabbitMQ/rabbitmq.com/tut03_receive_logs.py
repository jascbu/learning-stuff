#!/usr/bin/env python

import pika


"""
"""
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


"""
"""
channel.exchange_declare(exchange='logs',type='fanout')


"""
Create a queue:
  - a uniquely new queue on every declaration
    -- "exclusive True" means exclusive to the instance of the consumer so once the consumer disconnects delete the queue
  - a queue name defined by the rabbit server randomly
"""
result = channel.queue_declare(exclusive=True)


"""
"""
queue_name = result.method.queue


"""
Bind the queue to the "logs" exchange
"""
channel.queue_bind(exchange='logs',queue=queue_name)


"""
"""
print ' [*] Waiting for logs. To exit press CTRL+C'


"""
"""
def callback(ch, method, properties, body):
	print " [x] %r" % (body,)


"""
"""
channel.basic_consume(callback,queue=queue_name,no_ack=True)


"""
"""
channel.start_consuming() 
