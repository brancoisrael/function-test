import azure.functions as func
import requests 
import io
from azure.functions._thirdparty.werkzeug.datastructures import FileStorage

def get_file(req: func.HttpRequest, file_url:str, field_name:str):
    
    try:
        url = req.get_json().get(file_url)
        if not url:
            return
        
        extension = (url.split("/")[-1]).split(".")[-1]
        content_type = f'file/{extension}'
        content = io.BytesIO(requests.get(url).content)        
        
        return FileStorage(content_type=content_type,stream=content)
      
    except:
        return
    


