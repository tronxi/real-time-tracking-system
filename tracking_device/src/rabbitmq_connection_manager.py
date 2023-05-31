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
        self._init_exchanges()

    def _init_exchanges(self):
        channel = self._connection.channel()
        channel.exchange_declare(exchange=self._exchange_name,
                                 exchange_type='fanout')
        channel.close()

    def create_channel(self):
        return self._connection.channel()

    def publish(self, channel, body):
        channel.basic_publish(exchange=self._exchange_name,
                              routing_key='',
                              body=body)

    def close(self):
        self._connection.close()
