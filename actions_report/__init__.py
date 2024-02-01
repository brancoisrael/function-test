from actions_report.actions_service import service
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    return service.find(req=req)
    