import pika
import sys


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="topic_logs", exchange_type='topic')
result = channel.queue_declare(
    # let the server assign a random name for the new queue
    queue='',
    # this queue should be deleted after connection closed
    exclusive=True,
)
# fetch the random queue name
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange="direct_logs", queue=queue_name,
                       routing_key=severity)
print("[*] Waiting for messages. To exit press CTRL+C")
channel.basic_consume(queue=queue_name, auto_ack=True,
                      on_message_callback=callback)

channel.start_consuming()
