import azure.functions as func
import json
import ast
from storage_account.blob_storage import blob_storage
from ocr.model import OCR
from datetime import datetime
from base.abstract_service import AbstractService
from ocr.ocr_message import OCRMessage

class OCRService(AbstractService):

    def __init__(self) -> None:
        self.partition_key = 'ocr'

    def create (self,req: func.HttpRequest) -> func.HttpResponse:
        if 'image_front' not in req.files:
            return func.HttpResponse(
            json.dumps({'status':'Image Front not found.'}),
            status_code=400)        
    
        image_front = req.files['image_front']
        image_front_name = blob_storage.save_file(image_front)
        
        ocr = OCR()
        
        if 'image_back' in req.files:
            image_back = req.files['image_back']
            image_back_name = blob_storage.save_file(image_back)
            ocr.image_back = blob_storage.get_url_prefix()+image_back_name
        
        
        ocr.image_front = blob_storage.get_url_prefix()+image_front_name        
        ocr.created_at = datetime.now()

        return self.execute_create(req=req,model=ocr,message_broker=OCRMessage())
    
    def special_function(self,data):
        if 'ocr' in data:
            data['ocr'] = str(data['ocr'])
            
    def special_formater(self,elements):
        list = [e for e in elements if 'ocr' in e]
        for l in list:
            l['ocr'] = ast.literal_eval(l['ocr'])
            
        
    
service = OCRService()