import requests
import json
import azure.functions as func
from os import getenv
from background_check.background_check_message import BackGroundCheckMessage as message

URL = getenv('URL')
PASSWORD = getenv('BCC_PASSWD')

class BackgroundCheckService():
    
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
        
        return func.HttpResponse(
            body= resp.text,
            mimetype="application/json",
            status_code=resp.status_code)
        