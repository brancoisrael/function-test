import uuid
from datetime import datetime
from utils.status_enum import StatusEnum
class Liveness():
    
    def __init__(self) -> None:
        self.PartitionKey = 'liveness'
        self.RowKey = str(uuid.uuid4())
        self.created_at: datetime
        self.modified_at = datetime.now()
        self.video: str
        self.mouth_status = StatusEnum.queued.name
        self.mouth:str
        self.blinks_status = StatusEnum.queued.name
        self.blinks:str
        self.best_frame_status = StatusEnum.queued.name
        self.best_frame:str
        self.scene_status = StatusEnum.queued.name
        self.scene:str
        self.multiple_faces_status = StatusEnum.queued.name
        self.multiple_faces:str
        self.same_face_status = StatusEnum.queued.name
        self.same_face: str
        self.voice_recognition_status = StatusEnum.queued.name
        self.voice_recognition: str
        self.billing = False
        