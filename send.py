import pika


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# create queue
channel.queue_declare(queue="hello")
# queue name is specified in the routing_key param
channel.basic_publish(exchange="",
                      routing_key="hello",
                      body="Hello World!")
print(" [x] Sent 'Hello World'")
connection.close()
