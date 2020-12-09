import pika

#
#self.connection = pika.BlockingConnection(
    #pika.ConnectionParameters(host='localhost'))

# Establishing the connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))

# Creating the channel
channel = connection.channel()
# Declaring  our queue
channel.queue_declare(queue='rpc_queue')


# This is the function that us gonna execute during the RPC
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def on_request(ch, method, properties, body):
    n = int(body)

    print(" [.] fib(%s)" % n)

    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(correlation_id= \
                                                         properties.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] I am waiting for  RPC requests here....")
channel.start_consuming()
