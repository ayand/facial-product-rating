import json
import boto3
import time
import os

client = boto3.client('firehose')
firehose_stream = os.environ['firehoseStream']

def write_to_firehose(body):
    payload = json.dumps({
        "id": body["id"],
        "productId": body["productId"],
        "userId": body["userId"],
        "emotion": body["emotion"],
        "gender": body["gender"],
        "age": int(body["age"]),
        "timestamp": body["timestamp"]
    })
    print(payload)
    kinesis_payload = { "Data": payload }
    response = client.put_record(DeliveryStreamName=firehose_stream, Record=kinesis_payload)
    print("Finished writing")
    return response


def handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    body = json.loads(message)
    response = write_to_firehose(body)
    return response
