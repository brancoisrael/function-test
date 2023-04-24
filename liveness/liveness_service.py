import azure.functions as func
from storage_account.blob_storage import blob_storage
from liveness.model import Liveness
from datetime import datetime
from liveness.liveness_message import LivenessMessage as Message
from base.abstract_service import AbstractService
from os import path , remove
import base64
import uuid
import tempfile

TABLE_NAME = 'liveness'

class LivenessService(AbstractService):

    def __init__(self) -> None:
        self.partition_key = 'liveness'

    def create (self,req: func.HttpRequest) -> func.HttpResponse:
        if 'video' not in req.files:
            return func.HttpResponse(
            "Video not found.",
            status_code=400)        
        
        file = req.files['video']
        file_name = blob_storage.save_file(file)
        
        liveness = Liveness()
        liveness.video = blob_storage.get_url_prefix()+file_name
        liveness.created_at = datetime.now()
        
        return self.execute_create(req=req,model=liveness,message_broker=Message())
    
    def special_function(self,data):
       
       if 'best_frame_status' in data and data['best_frame_status'] == 'processed':
            byte_arr = base64.decodebytes(bytes(data['best_frame'],'UTF-8'))
            file_name='{}.{}'.format(uuid.uuid4(),'png')
            file_path=path.join(tempfile.gettempdir(),file_name)
            file = open(file_path,'wb')
            file.write(byte_arr)
            file.close()
            
            file_temp = open(file_path,'rb')
            blob_storage.upload_blob(file_temp, file_name,'image/png')
            file_temp.close()
            remove(file_path)
            
            data['best_frame']=blob_storage.get_url_prefix()+file_name
                
    def special_formater(self, elements):
        pass

service = LivenessService()