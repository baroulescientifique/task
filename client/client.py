import pika
import uuid

class FibonacciRpcClient(object):

    def __init__(self):

        #
        #self.connection = pika.BlockingConnection(
            #pika.ConnectionParameters(host='localhost'))

        # Start the connection again
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))

        # Create a channel
        self.channel = self.connection.channel()

        # Declare an empty queue
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None

        # here we need to make sure that we do have
        # an unique identifier
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

print(" [x] Launching a RPC call  fib(60)")
response = fibonacci_rpc.call(60)
print(" [.] Received  %r as the response from  the server" % response)