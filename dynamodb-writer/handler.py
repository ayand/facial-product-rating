import json
import boto3
import time
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb').Table(os.environ['DYNAMODB_TABLE'])

def write_to_dynamodb(body):
    payload = {
        "id": body["id"],
        "productId": body["productId"],
        "userId": body["userId"],
        "emotion": body["emotion"],
        "url": body["url"],
        "timestamp": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    }
    response = dynamodb.put_item(Item=payload)
    print("Finished writing")
    return response

def handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    body = json.loads(message)
    response = write_to_dynamodb(body)
    return response
