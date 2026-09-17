"""
DynamoDbWriter Lambda
---------------------
Writes a JSON payload into a DynamoDB table.
Reads table name from env var TABLE_NAME.
Requires IAM permission: dynamodb:PutItem
"""

import json
import logging
import os
import uuid
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]        # fail fast if missing
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    logger.info("Event: %s", json.dumps(event, default=str))

    # Accept either API Gateway style (body is a string) or direct JSON
    payload = event
    if isinstance(event.get("body"), str):
        try:
            payload = json.loads(event["body"])
        except json.JSONDecodeError:
            return _bad_request("Request body is not valid JSON")

    item_id = payload.get("id") or str(uuid.uuid4())
    item = {
        "id": item_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "data": payload,
    }

    try:
        table.put_item(Item=item)
        logger.info("Wrote item id=%s to %s", item_id, TABLE_NAME)
        return {
            "statusCode": 201,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"id": item_id, "table": TABLE_NAME}),
        }

    except ClientError as e:
        logger.exception("DynamoDB put_item failed")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }


def _bad_request(msg):
    return {
        "statusCode": 400,
        "body": json.dumps({"error": msg}),
    }

    