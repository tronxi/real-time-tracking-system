import pika
from pika import credentials


class RabbitmqConnection:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='tronxi.ddns.net',
                                      port=5672,
                                      credentials=credentials.PlainCredentials(
                                          username="rocket",
                                          password="rocket")))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='tracking_device_events',
                                      exchange_type='fanout')

    def publish(self, body):
        self.channel.basic_publish(exchange='tracking_device_events',
                                   routing_key='',
                                   body=body)

    def close(self):
        self.connection.close()
