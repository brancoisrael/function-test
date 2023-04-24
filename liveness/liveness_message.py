import azure.functions as func
from base.message_broker import MessageBroker

class LivenessMessage(MessageBroker):
    
    filas=[
        'mouth','blinks','best_frame',
        'scene','multiple_faces',
        'voice_recognition','monitor_request'
    ]
    
    def send(self,liveness:dict,req: func.HttpRequest):   
        
        message = {
                    "liveness_id": liveness['RowKey'],
                    "video_path": liveness['video'],
                    "token_type": "x-functions-key",
                    "token": self.get_token(req),
                    "ip_request":self.get_ip(req),
                    "algorithm":'1',
                    "callback":self.get_callback('liveness')}
        
        for fila in self.filas:
            self.publish(fila, message)