from os import getenv
from datetime import datetime
from azure.core.credentials import AzureNamedKeyCredential
from azure.data.tables import TableServiceClient
from azure.data.tables import TableServiceClient


AZURE_ACCOUNT_NAME = getenv('AZURE_STORAGE_ACCOUNT', 'sainovacao')
AZURE_ACCOUNT_KEY = getenv('AZURE_ACCOUNT_KEY', 'axgraMGHPVZ7remAx60ne376KBy717ENWsAz8q7Hc6iMDCEUVR9iB042GhUMIJwHYD5FFzMoJLl++AStUDNiFg==')

class Table():
    
    def __init__(self) -> None:
        credential = AzureNamedKeyCredential(name=AZURE_ACCOUNT_NAME,key=AZURE_ACCOUNT_KEY)
        self.table_service = TableServiceClient(endpoint=f'https://{AZURE_ACCOUNT_NAME}.table.core.windows.net', credential=credential)
        
        self.table_client = self.table_service.create_table_if_not_exists('live4safe')
            
    def save(self,entity):
        return self.table_client.create_entity(entity)
    
    def update(self,partition_key,row_key:str, data:dict):
        entity  = self.table_client.get_entity(partition_key=partition_key,row_key=row_key)
        for key in data.keys():
            entity[key] = data[key]
        entity['modified_at'] = datetime.now()
        self.table_client.update_entity(entity=entity)
    
    def find_by(self,filter:str):
        elements = self.table_client.query_entities(filter) 
        dict_elements = []
        for e in elements:
            e['modified_at'] =  e.get('modified_at')._service_value
            e['created_at'] =  e.get('created_at')._service_value
            dict_elements.append(e)
        return dict_elements
    
    
        
        