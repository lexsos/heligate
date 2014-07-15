import os
import pika
from subprocess import call
from django.conf import settings

from .settings import CONFIG


def run_scripts(scripts):
    old_cd = os.getcwd()

    rc_root = os.path.join(settings.PROJECT_ROOT, '..', 'rc.d')
    rc_root = os.path.normpath(os.path.abspath(rc_root))

    os.chdir(rc_root)
    for script in scripts:
        path = os.path.join(rc_root, script)
        call(path)
    os.chdir(old_cd)


def rabbit_connection():
    connection_parametrs = pika.ConnectionParameters(
        host=CONFIG['RABBIT_HOST'],
    )
    return pika.BlockingConnection(connection_parametrs)


def rabbit_channel(connection):
    channel = connection.channel()
    channel.exchange_declare(
        exchange=CONFIG['RABBIT_EXCHANGE'],
        type='fanout',
    )
    return channel


def rabbit_send(message):
    connection = rabbit_connection()
    channel = rabbit_channel(connection)
    channel.basic_publish(
        exchange=CONFIG['RABBIT_EXCHANGE'],
        routing_key='',
        body=message,
    )
    connection.close()


def rabbit_receive(channel, call_back):
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(
        exchange=CONFIG['RABBIT_EXCHANGE'],
        queue=queue_name,
    )
    channel.basic_consume(
        call_back,
        queue=queue_name,
        no_ack=True,
    )
