#!/usr/bin/env python

import pika
import sys


"""
Connect to RabbitMQ server
  - The below will establish a connection with a broker on the local machine
  - You could use a remote machine but swapping out 'localhost' for name or IP
"""
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


"""
Make sure recipient queue exists
  - If we send msg to non-existing queue then rabbit will drop it

TUT02
  - added 'Queue Durability'
  - renamed queue as can't redo properties on live queue without a rabbitmqctl stop_app / reset / start_app
"""
channel.queue_declare(queue = 'task_queue', durable=True)


"""
Create messages from args passed from cmd line
"""
message = ' '.join(sys.argv[1:]) or "Hello World!"


"""
Send a msg to the default exchange
The default exchange is 
  - defined by empty string: "exchange = ''"
  - implicitly bound to every queue
  - requires a routing key equal to the destination queue name
  - can not be explicitly bound to
  - can not be unbound from
  - can not be deleted


TUT02
  - Routing key changed because can't change properties on current queue without a reset so this is an easy fix
  - Body changed to pick up message passed from arguments
  - Added 'Message Durability / Persistence' with 'deliver_mode = 2' (NOTE: There is still a short window where msgs could be lost, just after RabbitMQ has accepted a msg but not saved it yet. It doesn't do 'fsync' for each message - it may be 'saved' but still in cache not on disk yet. Stronger guarentee achieved by wrapping publishes in a 'transaction'
"""
channel.basic_publish(exchange = '',
			routing_key = 'task_queue',
			body = message,
			properties=pika.BasicProperties(delivery_mode = 2))
print " [x] Sent %r" % (message,)


"""
Exit cleanly, making sure
  - network buffers are flushed
  - message actually delivered
"""
connection.close()
