import pika
from pika import credentials


class RabbitmqConnectionManager:

    def __init__(self):
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='tronxi.ddns.net',
                                      port=5672,
                                      credentials=credentials.PlainCredentials(
                                          username="rocket",
                                          password="rocket")))
        self._exchange_name = 'tracking_device_events'
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange=self._exchange_name,
                                       exchange_type='fanout')

    def publish(self, body):
        self._channel.basic_publish(exchange=self._exchange_name,
                                    routing_key='',
                                    body=body)

    def close(self):
        self._connection.close()
