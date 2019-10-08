import pika
import sys


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# assign a named exchange to channel and declare exchange type
channel.exchange_declare(exchange="topic_logs", exchange_type="topic")

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
msg = ' '.join(sys.argv[2:]) or "Hello World!"
channel.basic_publish(
    exchange="topic_logs",
    routing_key=routing_key,
    body=msg,
)
print(" [x] Sent %r:%r" % (routing_key, msg))
connection.close()
