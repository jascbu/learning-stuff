#!/usr/bin/env python

import pika
import sys

"""
Connect to RabbitMQ server
  - connection made to a broker
  - swap localhost for other IP/hostname
"""
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


"""
Ensure recipient Exchange exists
  - last time we declared queue, this time exchange, called "logs"
  - the type of exchange is "fanout" which is a broadcast to multiple queues

NOTE: we are not declaring a queue
  - because we are only interested in current flowing messages not old ones
  - so the consumers must declare and bind a queue to the exchange
  - if the consumers have not yet bound a queue then the messages will be lost but that is intended behaviour in this scenario
  - so running this script alone will register a publish on the "log" exchange graph but the message will then be dumped
"""
channel.exchange_declare(exchange='logs',
			type='fanout')


"""
Create a message 
  - from arguments passed from the command line
  - or if no args then use a static message 
"""
message = ' '.join(sys.argv[1:]) or "info: Hello World!"


"""
Publish a message
  - to the exchange "logs"
  - with a nul or default routing key therefore routing to the default queue which considering the "fanout" before of the exchange is all current queues in that exchange
"""
channel.basic_publish(exchange='logs',
			routing_key='',
			body=message)


"""
Print to stdout
  - a confirmation of passed message
"""
print " [x] Sent %r" % (message,)


"""
Exit cleanly
  - network buffers are flushed
  - messages are actualy delivered
"""
connection.close()
