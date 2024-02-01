import azure.functions as func
import json
from storage_account.table import Table
from base.message_broker import MessageBroker

class AbstractService():

    def execute_create (self, req: func.HttpRequest, model, message_broker:MessageBroker) -> func.HttpResponse:
        try:
            table = Table()
            table.save(model.__dict__)        
            
            model = table.find_by(f"RowKey eq '{model.RowKey}'")[0]
            
            message_broker.send(model,req)
            
            response = func.HttpResponse(
                body= json.dumps(model),
                mimetype="application/json",
                status_code=201)
            
        except Exception as ex:   
            response = func.HttpResponse(
            ex,status_code=400)
        
        return response
            
    def update (self,req: func.HttpRequest) -> func.HttpResponse:
        
        data = json.loads(req.get_body().decode("utf-8"))
        
        self.special_function(data) 
        
        table = Table()
        table.update(self.partition_key,req.params.get('RowKey'),data)
            
        return func.HttpResponse(
            body=json.dumps({'status':'updated'}),
            mimetype="application/json",
            status_code=200)
        
    def find (self,req: func.HttpRequest) -> func.HttpResponse:
        filter= f"PartitionKey eq '{self.partition_key}'"
        keys = list(req.params.keys())
        
        if len(keys)>0:
            filter = f"{filter} and {keys[0]} eq '{req.params.get(keys[0])}'"
        
        table = Table()
        elements = table.find_by(filter)
        
        self.special_formater(elements)
        
        if len(elements)==1:
            elements = elements[0]
            
        return func.HttpResponse(
            body=json.dumps(elements),
            mimetype="application/json",
            status_code=200)
        
    