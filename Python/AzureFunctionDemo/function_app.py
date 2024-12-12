import azure.functions as func
import logging
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="get_iss_position")
def get_iss_position(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Getting IIS position')
    response = requests.get('http://api.open-notify.org/iss-now.json')
    return func.HttpResponse(response.text, status_code=200)

