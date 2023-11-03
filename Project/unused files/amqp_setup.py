import pika
from os import environ
import time

#hostname = os.environ.get('AMQP_HOST', 'localhost')
#hostname = "rabbitmq" # default hostname
hostname = environ.get('rabbit_host') or 'rabbitmq'
port = 5672

# Wait for RabbitMQ to start up
connected = False
while not connected:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, heartbeat=3600, blocked_connection_timeout=3600))
        connected = True
    except pika.exceptions.AMQPConnectionError:
        print('RabbitMQ not available yet, waiting...')
        time.sleep(5)
        
channel = connection.channel()

exchangename="g10t2_topic"
exchangetype="topic"
channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)

queue_name = 'announcement'
channel.queue_declare(queue=queue_name, durable=True) 
    # 'durable' makes the queue survive broker restarts

#bind Error queue
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='*.msg') 

queue_name = 'promotion'
channel.queue_declare(queue=queue_name, durable=True) 
    # 'durable' makes the queue survive broker restarts

#bind Error queue
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='*.promo') 

"""
This function in this module sets up a connection and a channel to a local AMQP broker,
and declares a 'topic' exchange to be used by the microservices in the solution.
"""
def check_setup():
    # The shared connection and channel created when the module is imported may be expired, 
    # timed out, disconnected by the broker or a client;
    # - re-establish the connection/channel is they have been closed
    global connection, channel, hostname, port, exchangename, exchangetype

    if not is_connection_open(connection):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, heartbeat=3600, blocked_connection_timeout=3600))
    if channel.is_closed:
        channel = connection.channel()
        channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)


def is_connection_open(connection):
    # For a BlockingConnection in AMQP clients,
    # when an exception happens when an action is performed,
    # it likely indicates a broken connection.
    # So, the code below actively calls a method in the 'connection' to check if an exception happens
    try:
        connection.process_data_events()
        return True
    except pika.exceptions.AMQPError as e:
        print("AMQP Error:", e)
        print("...creating a new connection.")
        return False
    except pika.exceptions.StreamLostError:
        # Handle the exception and attempt to reconnect
        print("Connection lost. Attempting to reconnect...")
        return False