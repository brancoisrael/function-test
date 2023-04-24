import azure.functions as func
from base.message_broker import MessageBroker

class BackGroundCheckMessage(MessageBroker):
        
    def send(self,req: func.HttpRequest):   
        message = {"liveness_id": req.params.get('cpf'),
                   "token": self.get_token(req),
                   "ip_request":self.get_ip(req),
                   "algorithm":'4'}
        
        self.publish('monitor_request', message)