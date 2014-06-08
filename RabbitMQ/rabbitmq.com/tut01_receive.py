#!/usr/bin/env python

import pika

"""Connect to RabbitMQ server
The below will establish a connection with a broker on the local machine
You could use a remote machine but swapping out 'localhost' for name or IP
"""  
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


"""Make sure queue exists
  - creating a queue with "queue_declare" is idempotent
  - good practice as don't know if publisher or consumer starts first
"""
channel.queue_declare(queue='hello')


"""Subscribe a callback function to a queue
  - callback function is called by pika lib to receive msg
  - our function below will print msg content on screen
"""
def callback(ch, method, properties, body):
  print " [x] received %r" % (body,)


"""Assign queue to callback function
  - "hello" queue is assigned to our callback
"""
channel.basic_consume(callback,
			queue='hello',
			no_ack=True)


"""Create never ending loop
  - wait for data
  - run callback
"""
print ' [*] Waiting for messages. To exit press CTRL+C'
channel.start_consuming()
