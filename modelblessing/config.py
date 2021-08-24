import os


def get_event_url():
    event_url = os.environ.get("EVENT_URL", "")
    return event_url

def get_workflow_url():
    workflow_url = os.environ.get("WORKFLOW_URL", "")
    return workflow_url