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
channel.exchange_declare(exchange='direct_logs',type='direct')


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
Collect the log types to be used as routing_keys
  - collect arguments after the command
  - if none exist error out command format message
"""
severities = sys.argv[1:]
if not severities:
	print >> sys.stderr, "Usage: %s [info] [warning] [error]" % (sys.argv[0],)
	sys.exit(1)

"""
Bind the queue to the "logs" exchange
"""
for severity in severities:
	channel.queue_bind(exchange='direct_logs',queue=queue_name,routing_key=severity)


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
