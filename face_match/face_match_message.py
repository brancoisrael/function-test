import azure.functions as func
from base.message_broker import MessageBroker

class FaceMatchMessage(MessageBroker):
    
    filas=[
        'mouth','blinks','best_frame',
        'scene','same_face',
        'voice_recognition','monitor_request'
    ]
    
    def send(self,face_match:dict,req: func.HttpRequest):   
        
        message = {
                    "face_match_id": face_match['RowKey'],
                    "image_a": face_match['image_a'],
                    "image_b": face_match['image_b'],
                    "token_type": "x-functions-key",
                    "token": self.get_token(req),
                    "ip_request":self.get_ip(req),
                    "callback":self.get_callback('face_match')}
        
        self.publish('face_match', message)
        
        message = {"liveness_id": face_match['RowKey'],
                   "token": self.get_token(req),
                   "ip_request":self.get_ip(req),
                   "algorithm":'3'}
        
        self.publish('monitor_request', message)