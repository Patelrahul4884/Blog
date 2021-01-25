# amqps://ucfguvli:bIk2YhvIeWvn0PzSnbfpsFd3JOx43pXf@lionfish.rmq.cloudamqp.com/ucfguvli

import pika
import json

params=pika.URLParameters('amqps://ucfguvli:bIk2YhvIeWvn0PzSnbfpsFd3JOx43pXf@lionfish.rmq.cloudamqp.com/ucfguvli')

connection=pika.BlockingConnection(params)

channel=connection.channel()

def publish(method,body):
    properties=pika.BasicProperties(method)
    channel.basic_publish(exchange="",routing_key="user",body=json.dumps(body),properties=properties)

    