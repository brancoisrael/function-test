import azure.functions as func
import json
import ast
import re
from storage_account.blob_storage import blob_storage
from ocr.model import OCR
from datetime import datetime
from base.abstract_service import AbstractService
from ocr.ocr_message import OCRMessage
from utils.blob_file import get_file

class OCRService(AbstractService):

    def __init__(self) -> None:
        self.partition_key = 'ocr'

    def create (self,req: func.HttpRequest) -> func.HttpResponse:
        image_front = get_file(req=req,file_url='image_path_front',field_name='image_front')
        image_back = get_file(req=req,file_url='image_path_back',field_name='image_back')

        if 'image_front' not in req.files and image_front==None:
            return func.HttpResponse(
            json.dumps({'status':'Image Front not found.'}),
            status_code=400)        
    
        if image_front==None:
            image_front = req.files['image_front']
        image_front_name = blob_storage.save_file(image_front)
        
        ocr = OCR()
        
        if 'image_back' in req.files or image_back != None:
            if image_back == None:
                image_back = req.files['image_back']
            image_back_name = blob_storage.save_file(image_back)
            ocr.image_back = blob_storage.get_url_prefix()+image_back_name
        
        
        ocr.image_front = blob_storage.get_url_prefix()+image_front_name        
        ocr.created_at = datetime.now()

        return self.execute_create(
            req=req,model=ocr,
            message_broker=OCRMessage())
    
    def special_function(self,data):
        if 'ocr' in data:
            answer = data['ocr']
            cpf=re.findall(r'([0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2})',str(answer['text']))
            if len(cpf)>0:       
                data['cpf'] = cpf.__getitem__(0)
            data['ocr'] = str(data['ocr'])
            
    def special_formater(self,elements):
        list = [e for e in elements if 'ocr' in e]
        for l in list:
            l['ocr'] = ast.literal_eval(l['ocr'])
            
        
    
service = OCRService()