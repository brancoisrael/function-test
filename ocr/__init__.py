import azure.functions as func
from ocr.ocr_service import service

function_app={
    'GET': service.find,
    'POST': service.create,
    'PUT': service.update
}

def main(req: func.HttpRequest) -> func.HttpResponse:    
    return function_app.get(req.method)(req=req)

