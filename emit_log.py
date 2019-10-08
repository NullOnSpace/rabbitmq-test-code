import pika
import sys


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# assign a named exchange to channel and declare exchange type
channel.exchange_declare(exchange="logs", exchange_type="fanout")
# queue name is specified in the routing_key param
msg = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(
    exchange="logs",
    routing_key="",  # this will be ignored since exchange type is fanout
    body=msg,
)
print(" [x] Sent %r" % msg)
connection.close()
