import jwt, json
import requests

from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, JsonResponse

from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header, BaseAuthentication
import pika
import uuid


SECRET_KEY_DEMO = 'qwertyuiopsdfghjklzxcvbnm'

class GetEmailToken(object):

    def __init__(self):
        self.params=pika.URLParameters('amqps://ucfguvli:bIk2YhvIeWvn0PzSnbfpsFd3JOx43pXf@lionfish.rmq.cloudamqp.com/ucfguvli')
        self.connection = pika.BlockingConnection(self.params)

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, email):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=email)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            msg = 'Invalid Method of token passing.'
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            if token=="null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)
        
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        # payload = jwt.decode(token, SECRET_KEY_DEMO, algorithm='HS256')
        payload = jwt.decode(jwt=token, key=SECRET_KEY_DEMO, algorithms=['HS256'])
        email = payload['email']
        
        try:
            token_rpc=GetEmailToken()
            print("Requesting For token")
            response=token_rpc.call(email)
            response_token=str(response)[2:-1]
            # data=requests.post("http://docker.for.mac.localhost:8001/api/user/get_token/",data={"email":email})
            # data=data.json()
            # a_token=data['token']
            if response_token != str(token):
                msg = {'Error': "Token mismatch or Expired",'status' :"401"}
                raise exceptions.AuthenticationFailed(msg)
               
        except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
            return HttpResponse({'Error': "Token is invalid"}, status="403")

        return (email,token)

    def authenticate_header(self, request):
        return 'Token'