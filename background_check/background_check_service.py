import requests
import json
import azure.functions as func
import uuid
from datetime import datetime
from os import getenv
from background_check.background_check_message import BackGroundCheckMessage as message
from storage_account.table import Table

URL = getenv('URL')
#URL = getenv('URL','http://localhost:8000')

PASSWORD = getenv('BCC_PASSWD','U#aBrpd5873P!@sdRCMQW')

class BackgroundCheckService():
    
    def __init__(self):
         self.partition_key = 'background_check'
    
    def find_cpf(self,req: func.HttpRequest):      
        if 'cpf' not in req.params:
            return func.HttpResponse(
                json.dumps({'mensagem':'CPF not found in query string.'}),
                mimetype="application/json",
                status_code=400)     
              
        data = {'username':'azure','password':PASSWORD}
        resp = requests.post(f'{URL}/api-token-auth/',data=data)
        
        if resp.status_code != 200:
            return resp
        
        message().send(req)
        token = json.loads(resp.text)['token']
        headers = {'Authorization': f'token {token}'}
        resp = requests.get(f"{URL}/background_check/{req.params.get('cpf')}",headers=headers)
       
        data = json.loads(resp.text)
        data['PartitionKey']=self.partition_key
        data['RowKey']=str(uuid.uuid4())
        data['created_at']=datetime.now()
        data['modified_at']=data['created_at']
        data['billing']=False
        table = Table()
        table.save(data)       
        
        data['created_at'] = str(data['created_at'])
        data['modified_at'] = str(data['created_at'])
        
        return func.HttpResponse(
            body= json.dumps(data),
            mimetype="application/json",
            status_code=resp.status_code)
        