import uuid
from datetime import datetime
from utils.status_enum import StatusEnum

class OCR():
    
    def __init__(self) -> None:
        self.PartitionKey = 'ocr'
        self.RowKey = str(uuid.uuid4())
        self.created_at: datetime
        self.modified_at = datetime.now()
        self.image_front: str
        self.image_back:str
        self.cpf:str
        self.ocr:list
        self.ocr_status = StatusEnum.queued.name
        self.billing = False
        