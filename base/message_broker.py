import azure.functions as func
import pika
import json
from os import getenv

RABBITMQ_HOST = getenv('RABBITMQ_HOST','rabbitmq-tcp.titcs-devops.com.br')
RABBITMQ_PORT = getenv("RABBITMQ_PORT", "5672")
RABBITMQ_PASSWD = getenv("RABBITMQ_PASSWD", "U#aBrpd5873P!@sdRCMQW")
FUNCTION_APP = getenv("FUNCTION_APP","fapp-inovacao")

class MessageBroker():
    
    def publish(self,method, message=None):
        credentials = pika.PlainCredentials('azure-functions',RABBITMQ_PASSWD,False)
        params = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT,credentials=credentials)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue=method)
        channel.basic_publish(exchange="", routing_key=method, body=json.dumps(message))
        connection.close()
        
    def get_ip(self,req: func.HttpRequest)->str:
        ip = '127.0.0.1'
        
        if "x-forwarded-for" in req.headers:
            ip = req.headers["x-forwarded-for"].split(':')[0]
        
        return ip
    
    def get_token(self, req: func.HttpRequest)->str:
        return req.headers['x-functions-key'] 
    
    def get_callback(self,endpoint:str)->str:
        #return f'http://localhost:7071/api/{endpoint}?RowKey='
        return f'https://{FUNCTION_APP}.azurewebsites.net/api/{endpoint}?RowKey='