# Import libraries
import base64
import json
import logging
import os
from typing import Dict

import boto3

logger = logging.getLogger(__name__)


# - PROJECT_NAME: Lookout project name to invoke
PROJECT_NAME = os.environ["PROJECT_NAME"]
lookout_client = boto3.client("lookoutvision")


def lambda_handler(event: Dict, context: Dict) -> Dict:
    """Main entry function.
    Args:
        event:      API Gateway event
        context:    Context attributes
    Returns:
        output (json): returning success or failure
    Examples:
    """
    response_headers = {
        "Access-Control-Allow-Origin": event["headers"]["origin"],
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST"
    },

    logger.info({
        "message": "Received event",
        "event": event,
    })

    try:
        body = json.loads(event["body"])
        body_bytes = body["image"].split(",")[-1]
        body_bytes = base64.b64decode(body_bytes)

        logger.info({
            "message": "Calling Lookout for Vision",
            "project_name": PROJECT_NAME,
            "body": body_bytes
        })

        response = lookout_client.detect_anomalies(
            ProjectName=PROJECT_NAME,
            ModelVersion='1',
            Body=body_bytes,
            ContentType='image/jpeg'
        )
        return {
            "statusCode": 200,
            "headers": response_headers,
            "body": json.dumps({
                "Confidence": f'{round(response["DetectAnomalyResult"]["Confidence"]*100, 2)}%'
            })
        }

    except Exception as e:
        logger.exception({
            "message": "Error occurred when processing event",
        })
        return {
            "statusCode": 400,
            "headers": response_headers,
            "message": json.dumps(e),
        }
