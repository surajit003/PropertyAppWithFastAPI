import json

import boto3
import botocore

import settings

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=settings.AWS_SECRET_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    region_name=settings.AWS_REGION,
)


class BotoClientException(Exception):
    pass


async def create_log(data):
    try:
        table = dynamodb.Table("Log")
        trans = {
            "log_id": data["log_id"],
            "request_ip": data["request_ip"],
            "message": json.dumps(data["message"]),
        }
        return table.put_item(trans)
    except botocore.exceptions.ClientError as e:
        raise BotoClientException(e)
