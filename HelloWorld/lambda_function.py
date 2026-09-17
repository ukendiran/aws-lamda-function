"""
HelloWorld Lambda
-----------------
Basic echo handler. Used to verify the CI/CD pipeline end-to-end.
"""

import json
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event, default=str))

    body = {
        "message": "Hello from Lambda!",
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "function_name": context.function_name,
        "function_version": context.function_version,
        "request_id": context.aws_request_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "echo": event,
    }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }