# amqps://ucfguvli:bIk2YhvIeWvn0PzSnbfpsFd3JOx43pXf@lionfish.rmq.cloudamqp.com/ucfguvli

import pika, json, os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE',"blog.settings")
django.setup()


params=pika.URLParameters('amqps://ucfguvli:bIk2YhvIeWvn0PzSnbfpsFd3JOx43pXf@lionfish.rmq.cloudamqp.com/ucfguvli')

connection=pika.BlockingConnection(params)

channel=connection.channel()

channel.queue_declare(queue='blog')

def callback(ch,method,properties,body):
    print("Received in blog")
    data = json.loads(body)


channel.basic_consume(queue='blog',on_message_callback=callback,auto_ack=True)
print('Started Consuming')

channel.start_consuming()

channel.close()
