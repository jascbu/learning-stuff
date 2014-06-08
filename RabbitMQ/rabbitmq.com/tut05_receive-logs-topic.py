#!/usr/bin/env python

import pika
import sys

"""
"""
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


"""
Create a connection from the channel to the exchange's queues
  - declare name of exchange
  - declare type of queue to be used
"""
channel.exchange_declare(exchange='topic_logs',type='topic')


"""
Create a queue:
  - a uniquely new queue on every declaration
    -- "exclusive True" means exclusive to the instance of the consumer so once the consumer disconnects delete the queue
  - a queue name defined by the rabbit server randomly
"""
result = channel.queue_declare(exclusive=True)


"""
Ask Rabbit server to give the queue a random name
"""
queue_name = result.method.queue


"""
Collect the <facility>.<severity> from the command arguments to use as routing_keys
  - collect arguments after the command
  - if none exist error out command format message
"""
binding_keys = sys.argv[1:]
if not binding_keys:
	print >> sys.stderr, "Usage: %s [binding_key]..." % (sys.argv[0],)
	sys.exit(1)

"""
Bind the queue to the "logs" exchange
"""
for binding_key in binding_keys:
	channel.queue_bind(exchange='topic_logs',queue=queue_name,routing_key=binding_key)


"""
"""
print ' [*] Waiting for logs. To exit press CTRL+C'


"""
"""
def callback(ch, method, properties, body):
	print " [x] %r:%r" % (method.routing_key, body,)


"""
"""
channel.basic_consume(callback,queue=queue_name,no_ack=True)


"""
"""
channel.start_consuming() 
