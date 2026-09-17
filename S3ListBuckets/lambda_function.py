"""
S3ListBuckets Lambda
--------------------
Lists all S3 buckets in the account. Demonstrates boto3 usage.
Requires IAM permission: s3:ListAllMyBuckets
"""

import json
import logging
import os

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")


def lambda_handler(event, context):
    logger.info("Event: %s", json.dumps(event, default=str))

    try:
        response = s3.list_buckets()
        buckets = [
            {
                "name": b["Name"],
                "creation_date": b["CreationDate"].isoformat(),
            }
            for b in response.get("Buckets", [])
        ]

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "environment": os.getenv("ENVIRONMENT", "unknown"),
                "bucket_count": len(buckets),
                "buckets": buckets,
            }),
        }

    except ClientError as e:
        logger.exception("S3 list_buckets failed")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }