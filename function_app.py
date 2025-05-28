import azure.functions as func
import logging
import uuid
from azure.functions.decorators.core import DataType

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="HttpExample")
@app.generic_output_binding(
    arg_name="toDoItems",
    type="sql",
    CommandText="dbo.ToDo",
    ConnectionStringSetting="SqlConnectionString",
    data_type=DataType.STRING
)
def HttpExample(req: func.HttpRequest, toDoItems: func.Out[func.SqlRow]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}
        name = req_body.get('name')

    if name:
        # binding to SQL output
        toDoItems.set(func.SqlRow({
            "Id": str(uuid.uuid4()),
            "title": name,
            "completed": False,
            "url": ""
        }))
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully and was saved to SQL.")
    else:
        return func.HttpResponse(
            "Please pass a name in the query string or in the request body.",
            status_code=400
        )