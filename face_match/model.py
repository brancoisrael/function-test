import uuid
from datetime import datetime
from utils.status_enum import StatusEnum

class FaceMatch():
    
    def __init__(self) -> None:
        self.PartitionKey = 'facematch'
        self.RowKey = str(uuid.uuid4())
        self.created_at: datetime
        self.modified_at = datetime.now()
        self.image_a: str
        self.image_b:str
        self.face_match_status = StatusEnum.queued.name
        self.face_match: bool
        self.billing = False