import serverless_wsgi
from truereadapi import wsgi

def handler(event, context):
    """
    This function is the actual Lambda entry point defined in template.yaml.
    It passes the event/context to the serverless_wsgi wrapper.
    """
    return serverless_wsgi.handle_request(wsgi.application, event, context)