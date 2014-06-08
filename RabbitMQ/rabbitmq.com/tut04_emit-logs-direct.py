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
  - last time we declared queue, this time exchange, called "direct_logs"
  - the type of exchange is "direct" so messages must be direct to one or more specific queues

NOTE: we are not declaring a queue
  - because we are only interested in current flowing messages not old ones
  - so the consumers must declare and bind a queue to the exchange
  - if the consumers have not yet bound a queue then the messages will be lost but that is intended behaviour in this scenario
  - so running this script alone will register a publish on the "direct_logs" exchange graph but the message will then be dumped
"""
channel.exchange_declare(exchange='direct_logs',
			type='direct')


"""
We need a variable to supply the "routing key", we are using "severity"
  - this will take the first argument after the command name
  - presuming the number of arguments is 1 or more, otherwise the "severity" will be default to 'info'
"""
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'


"""
Create a message 
  - from the 2nd and higher arguments passed in on the command line
  - or if there was not a 2nd or higher argument use the default message 'Hello World!'
  - NOTES: Previously we used the first argument as the message but we have repurposed that to be the value of the "severity" variable to use as a routing key
"""
message = ' '.join(sys.argv[2:]) or 'Hello World!'


"""
Publish a message
  - to the exchange "direct_logs"
  - with a routing_key set by the value of the variable severity which will be our log level and therefore allows consumers to subscribe to a certain level of logs
"""
channel.basic_publish(exchange='direct_logs',
			routing_key=severity,
			body=message)


"""
Print to stdout
  - a confirmation of passed message
"""
print " [x] Sent %r:%r" % (severity, message,)


"""
Exit cleanly
  - network buffers are flushed
  - messages are actualy delivered
"""
connection.close()
