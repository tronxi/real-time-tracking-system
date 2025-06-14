import pika
from pika import credentials


class RabbitmqConnectionManager:

    def __init__(self):
        self._connection = None
        self._channel = None
        self._exchange_name = 'tracking_device_events'
        try:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='tronxi.ddns.net',
                    port=5672,
                    credentials=credentials.PlainCredentials(
                        username="rocket",
                        password="rocket"
                    )
                )
            )
            self._channel = self._connection.channel()
            self._channel.exchange_declare(exchange=self._exchange_name, exchange_type='fanout')
        except Exception as e:
            print(f"Could not connect to RabbitMQ: {e}")

    def publish(self, body):
        if self._channel:
            try:
                self._channel.basic_publish(exchange=self._exchange_name, routing_key='', body=body)
            except Exception as e:
                print(f"Failed to publish message: {e}")

    def close(self):
        if self._connection:
            try:
                self._connection.close()
            except Exception as e:
                print(f"Failed to close RabbitMQ connection: {e}")
