from base.abstract_service import AbstractService
from storage_account.table import Table
import azure.functions as func
import json
import re
from azure.data.tables import TableClient
from os import getenv
from datetime import datetime
from azure.core.credentials import AzureNamedKeyCredential
from azure.data.tables import TableServiceClient

from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from datetime import datetime

AZURE_ACCOUNT_NAME = getenv('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = getenv('AZURE_ACCOUNT_KEY')

class ActionsReportService():
       
    
    def __init__(self) -> None:
        self.table_service = TableService(account_key=AZURE_ACCOUNT_KEY,account_name=AZURE_ACCOUNT_NAME)

    def find (self,req: func.HttpRequest) -> func.HttpResponse:
        keys = list(req.params.keys())
        num_rows = 10
        marker = None
        
        if 'PartitionKey' not in keys:
            return func.HttpResponse(
            body=json.dumps({'error':'Request must contain PartitionKey to continue.'}),
            mimetype="application/json",
            status_code=428)        
        
        filter = f"PartitionKey eq '{req.params.get('PartitionKey')}' and "
        
        if 'RowKey' in keys:
            filter += f"RowKey eq '{req.params.get('RowKey')}' and "
        
        if 'DateInit' in keys and 'DateEnd' in keys:
            filter += f"modified_at ge datetime'{req.params.get('DateInit')}' and modified_at le datetime'{req.params.get('DateEnd')}' and "
        
        if 'NumRows' in keys:
            num_rows = req.params.get('NumRows')
        
        if 'nextpartitionkey' in keys and 'nextrowkey' in keys:
            marker ={
                'nextpartitionkey':req.params.get('nextpartitionkey'),
                'nextrowkey':req.params.get('nextrowkey')
            }    
        
        filter = filter[:-5]
                
        query_results = self.table_service.query_entities(
            table_name='live4safe',
            filter=filter,
            num_results=int(num_rows), 
            marker=marker)
        marker=query_results.next_marker
            
        dict_elements = []  
        for entity in query_results:
            entity['modified_at'] = entity.get('modified_at').strftime('%Y-%m-%d %H:%M:%S')
            entity['created_at'] =  entity.get('created_at').strftime('%Y-%m-%d %H:%M:%S')
            
            if 'blinks' in entity:
                entity['blinks'] = entity.get('blinks').value
            
            if 'mouth' in entity:
                entity['mouth'] = entity.get('mouth').value
                
            if 'multiple_faces' in entity:
                entity['multiple_faces'] = entity.get('multiple_faces').value
            
            if 'situation_code' in entity:
                entity.pop('situation_code')          
            
            entity.pop('Timestamp')
            entity.pop('etag')               
            dict_elements.append(entity)    
        
        dict_elements = sorted(dict_elements, reverse=True, key=lambda entity: entity.get('created_at') )
        dict_elements.append(marker)      
        return func.HttpResponse(
            body=json.dumps(dict_elements),
            mimetype="application/json",
            status_code=200)
        
    
    
service = ActionsReportService()