#!/usr/bin/env python

import pika


"""Connect to RabbitMQ server
The below will establish a connection with a broker on the local machine
You could use a remote machine but swapping out 'localhost' for name or IP
"""
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


"""Make sure recipient queue exists
If we send msg to non-existing queue then rabbit will drop it
"""
channel.queue_declare(queue = 'hello')


"""Send a msg to the default exchange
The default exchange is 
  - defined by empty string: "exchange = ''"
  - implicitly bound to every queue
  - requires a routing key equal to the destination queue name
  - can not be explicitly bound to
  - can not be unbound from
  - can not be deleted
"""
channel.basic_publish(exchange = '',
			routing_key = 'hello',
			body = 'hello world!')
print "[x] Sent 'hello world!'"


"""Exit cleanly, making sure
  - network buffers are flushed
  - message actually delivered
"""
connection.close()
