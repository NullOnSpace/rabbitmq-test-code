import pika
import sys


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# create queue
# durable=True declares the queue to be persistent
channel.queue_declare(queue="task_queue", durable=True)
# queue name is specified in the routing_key param
msg = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange="",
    routing_key="task_queue",
    body=msg,
    # mark messages as persistent
    properties=pika.BasicProperties(delivery_mode=2),
)
print(" [x] Sent %r" % msg)
connection.close()
