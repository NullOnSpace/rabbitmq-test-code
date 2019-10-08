import pika
import sys


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="direct_logs", exchange_type='direct')
result = channel.queue_declare(
    # let the server assign a random name for the new queue
    queue='',
    # this queue should be deleted after connection closed
    exclusive=True,
)
# fetch the random queue name
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange="direct_logs", queue=queue_name,
                       routing_key=severity)
print("[*] Waiting for messages. To exit press CTRL+C")
channel.basic_consume(queue=queue_name, auto_ack=True,
                      on_message_callback=callback)

channel.start_consuming()
