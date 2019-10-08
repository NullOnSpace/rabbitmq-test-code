import pika
import time


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    # send a proper acknowledgement from worker
    channel.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
# create queue to ensure this queue's existence, this is idempotent
channel.queue_declare(queue="task_queue", durable=True)
print("[*] Waiting for messages. To exit press CTRL+C")
# prefetch_count=1 means that don't dispatch a message to worker until
# it has processed and acknowledged the previous one
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
