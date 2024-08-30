import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="AZFuncActivator")
def AZFuncActivator(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # SI: primero preguntar si es RVC o mi postulacion va a ser RVC; Si lo es entonces postular

        # Preguntar si viene con Tarjeta digital y mandarla a crear

    # NO: entonces seria compra de producto 


    # Publicar mensaje de Activacion de productos en plataformas




    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )