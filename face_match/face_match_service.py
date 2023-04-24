import azure.functions as func
import json
from storage_account.blob_storage import blob_storage
from face_match.model import FaceMatch
from datetime import datetime
from base.abstract_service import AbstractService
from face_match.face_match_message import FaceMatchMessage

class FaceMatchService(AbstractService):

    def __init__(self) -> None:
        self.partition_key = 'facematch'

    def create (self,req: func.HttpRequest) -> func.HttpResponse:
        if 'image_a' not in req.files or 'image_b' not in req.files:
            return func.HttpResponse(
            json.dumps({'status':'Image A or B not found.'}),
            status_code=400)        
    
        image_a = req.files['image_a']
        image_a_name = blob_storage.save_file(image_a)
        
        image_b = req.files['image_b']
        image_b_name = blob_storage.save_file(image_b)
        
        face_match = FaceMatch()
        face_match.image_a = blob_storage.get_url_prefix()+image_a_name
        face_match.image_b = blob_storage.get_url_prefix()+image_b_name
        face_match.created_at = datetime.now()

        return self.execute_create(req=req,model=face_match,message_broker=FaceMatchMessage())
    
    def special_function(self,data):
        pass

    def special_formater(self, elements):
        pass


service = FaceMatchService()