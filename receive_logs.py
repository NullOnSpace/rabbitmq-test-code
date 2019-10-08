import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.exchange_declare(exchange="logs", exchange_type='fanout')
result = channel.queue_declare(
    # let the server assign a random name for the new queue
    queue='',
    # this queue should be deleted after connection closed
    exclusive=True,
)
# fetch the random queue name
queue_name = result.method.queue
channel.queue_bind(exchange="logs", queue=queue_name)
print("[*] Waiting for messages. To exit press CTRL+C")
channel.basic_consume(queue=queue_name, auto_ack=True,
                      on_message_callback=callback)
channel.start_consuming()
