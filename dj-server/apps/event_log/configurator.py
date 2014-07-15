import json

from .event import apply_events
from .utils import (
    rabbit_connection,
    rabbit_channel,
    rabbit_receive,
)


def message_receiver(ch, method, properties, body):
    data = json.loads(body)
    apply_events(data['events'])


def run():
    connection = rabbit_connection()
    channel = rabbit_channel(connection)
    rabbit_receive(channel, message_receiver)
    channel.start_consuming()
