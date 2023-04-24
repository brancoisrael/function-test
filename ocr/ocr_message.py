import azure.functions as func
from storage_account.blob_storage import blob_storage
from base.message_broker import MessageBroker

class OCRMessage(MessageBroker):
    
    def send(self,ocr:dict,req: func.HttpRequest):   
        
        images = [ocr['image_front']]
        if 'image_back' in ocr:
            images.append(ocr['image_back'])
        
        message = {"ocr_id":ocr['RowKey'],
                   "images": images,
                   "token_type": "x-functions-key",
                   "token": self.get_token(req),
                   "ip_request":self.get_ip(req),
                   "callback":self.get_callback('ocr')}       
        
        self.publish('ocr', message)

        message = {"liveness_id": ocr['RowKey'],
                   "token": self.get_token(req),
                   "ip_request":self.get_ip(req),
                   "algorithm":'2'}
        
        self.publish('monitor_request', message)
        