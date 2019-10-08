import pika
import sys


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# assign a named exchange to channel and declare exchange type
channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
msg = ' '.join(sys.argv[2:]) or "Hello World!"
channel.basic_publish(
    exchange="direct_logs",
    routing_key=severity,
    body=msg,
)
print(" [x] Sent %r:%r" % (severity, msg))
connection.close()
