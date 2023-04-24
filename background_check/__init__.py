import azure.functions as func
from background_check.background_check_service import BackgroundCheckService as service

def main(req: func.HttpRequest) -> func.HttpResponse:
    return service().find_cpf(req)