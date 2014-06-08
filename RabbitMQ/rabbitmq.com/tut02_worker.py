#!/usr/bin/env python

import pika
import time

"""
Connect to RabbitMQ server
  - The below will establish a connection with a broker on the local machine
  - You could use a remote machine but swapping out 'localhost' for name or IP
"""  
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


"""
Make sure queue exists
  - creating a queue with "queue_declare" is idempotent
  - good practice as don't know if publisher or consumer starts first

TUT02
  - added 'Queue Durability'
  - renamed queue as can't redo properties on live queue without a rabbitmqctl stop_app / reset / start_app
"""
channel.queue_declare(queue='task_queue', durable=True)


"""
"""
print ' [*] Waiting for messages. To exit CTRL+C'


"""
Subscribe a callback function to a queue
  - callback function is called by pika lib to receive msg
  - our function below will print msg content on screen

TUT02
  - added a way to fake work done with time sleep based on number of 'dots'
  - removed 'no_ack=True' flag to allow acks from consumers (NOTE: consumer must die before rabbit redistributes msg, there is no timeout)
"""
def callback(ch, method, properties, body):
  print " [x] received %r" % (body,)
  time.sleep( body.count('.') )
  print " [x] Done"
  ch.basic_ack(delivery_tag = method.delivery_tag)


"""
TUT02
  - Added "qos" because default is to give Nth msg to Nth consumer so in roundrobin if msgs odd/even light/heavy, one consumer always slow. "prefetch_count=1" means don't dispatch til consumer has processed and acknowledged previous 1, and therefore dispathe to next available consumer.
"""
channel.basic_qos(prefetch_count=1)


"""
Assign queue to callback function
  - "hello" queue is assigned to our callback
"""
channel.basic_consume(callback,
			queue='task_queue')


"""
Create never ending loop
  - wait for data
  - run callback
"""
print ' [*] Waiting for messages. To exit press CTRL+C'
channel.start_consuming()
