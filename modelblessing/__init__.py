# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json

import azure.functions as func
import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):
    headers = {"Content-Type": "application/json"}
    event_url = "https://developervelocity.azurewebsites.net/api/modelblessingeventtrigger?code=SnCkWJ0rP9N8EEBcgd8w/esSHzGfSNGIKYdigvIYbx9GlRHGTJ4sFQ=="
    body = {
        "instance_id": context._instance_id,
        "event_url": event_url
    }
    _ = yield context.call_http('POST', 'https://prod-219.westeurope.logic.azure.com:443/workflows/0458b7f853f9473d8950e0f411c5c929/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=P6wa-MLpVUn56F3yODwu80Ig1IES2_dLL8-tpUrG9xM', content=body, headers=headers)
    teams_response = context.wait_for_external_event("blessing")
    #TODO add timer
    result = yield context.task_any([teams_response])
    print(result.result)
    second_response = yield context.call_activity('activity-after-longrunning-task')
    return second_response


main = df.Orchestrator.create(orchestrator_function)
