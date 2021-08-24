import azure.functions as func
import azure.durable_functions as df
import config
from datetime import timedelta


def orchestrator_function(context: df.DurableOrchestrationContext):
    headers = {"Content-Type": "application/json"}
    body = {
        "instance_id": context._instance_id,
        "event_url": config.get_event_url()
    }
    _ = yield context.call_http('POST', config.get_workflow_url(), content=body, headers=headers)

    expiration = context.current_utc_datetime + timedelta(hours=24)
    timeout_task = context.create_timer(expiration)

    teams_response = context.wait_for_external_event("blessing")
    result = yield context.task_any([teams_response, timeout_task])
    print(result.result)
    second_response = yield context.call_activity('activity-after-longrunning-task')
    return second_response


main = df.Orchestrator.create(orchestrator_function)