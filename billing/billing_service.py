import pytz, asyncio
from datetime import datetime
from os import getenv
from base.abstract_service import AbstractService,MessageBroker
from storage_account.table import Table

PLAN_TYPE = getenv('PLAN_TYPE')
MANAGED_RESOURCE = getenv('MANAGED_RESOURCE')

class BillingService(AbstractService,MessageBroker):
    
    def __init__(self)->None:
        self.partition_keys = [
            'facematch',
            'ocr',
            'background_check',
            'liveness'
        ]        
    
        
    def check_billing(self):
        table = Table()
        date = datetime.now(pytz.utc)
        request = []
        results=[]        
        for key in  self.partition_keys:
            filter = f"PartitionKey eq '{key}' and billing eq false"
            result=table.find_by(filter=filter)
            results.extend(result)
            if(len(result)>0):
                resource = {
                    'resourceUri': MANAGED_RESOURCE,
                    'quantity': len(result),
                    'dimension': key,
                    'effectiveStartTime': date.strftime('%Y-%m-%dT%H:%M:%S'),
                    'planId':PLAN_TYPE
                }
                request.append(resource)
        
        if len(request) > 0:
            asyncio.run(self.publish('billing', request))    
            
            for element in results:
                element['billing']=True
                table.update(element['PartitionKey'],element['RowKey'], element)
        
service = BillingService()