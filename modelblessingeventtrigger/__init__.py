# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt
import azure.functions as func
import azure.durable_functions as df

# async def main(instance_id:str, starter: str) -> func.HttpResponse:
#     client = df.DurableOrchestrationClient(starter)
#     await client.raise_event(instance_id, 'blessing', True)


# This function an HTTP starter function for Durable Functions.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable activity function (default name is "Hello")
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt
 
import logging

import azure.functions as func
import azure.durable_functions as df


async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    req_body = req.get_json()
    instance_id = req_body.get("instance_id")
    is_blessed = req_body.get("is_blessed")
    logging.warning(is_blessed)
    await client.raise_event(instance_id, 'blessing', is_blessed)
    return "Succeeded raising event"