import azure.functions as func
import pika
import json
from os import getenv
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

FUNCTION_APP = getenv("FUNCTION_APP")
EVENT_HUB_CONNECTION_STR = getenv('EVENT_HUB_CONNECTION_STR')


class MessageBroker():
        
    async def publish(self,eventhub_name,message):
        self.producer = EventHubProducerClient.from_connection_string(
            conn_str=EVENT_HUB_CONNECTION_STR,
            eventhub_name= eventhub_name
        ) 
        async with self.producer:                 
            event_data = await self.producer.create_batch()
            event = EventData(json.dumps(message))
            event.body_as_json(encoding='UTF-8')
            event_data.add(event)
            await self.producer.send_batch(event_data)
            
        
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