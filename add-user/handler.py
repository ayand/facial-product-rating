import json
import boto3
import time
import os
from datetime import datetime, timezone

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb').Table(os.environ['DYNAMODB_TABLE'])
bucket_name = os.environ['S3_BUCKET']
collection = os.environ['FACIAL_RATING_COLLECTION']

def extract_data(event):
    body = json.loads(event['body'])

    user_id = body['userID']
    key = body['key']

    return (user_id, key)


def detect_faces(bucket_name, key):
    facial_analysis = rekognition.detect_faces(Image={'S3Object':{'Bucket':bucket_name,'Name':key}},Attributes=['ALL'])
    faces = facial_analysis["FaceDetails"]
    return faces


def add_face_to_collection(bucket_name, key):
    face_addition_response = rekognition.index_faces(
        CollectionId=collection,
        Image={'S3Object':{'Bucket':bucket_name,'Name':key}},
        ExternalImageId=key,
        MaxFaces=1
    )
    faceRecord = face_addition_response['FaceRecords'][0]
    face_id = faceRecord['Face']['FaceId']
    return face_id


def record_face_collection_id(user_id, face_id):
    timestamp = datetime.now(timezone.utc).strftime("%m/%d/%Y, %H:%M:%S")

    body = {
        "id": user_id,
        "face_id": face_id,
        "timestamp": timestamp
    }

    response = dynamodb.put_item(Item=body)
    print("Finished writing")
    return body


def handler(event, context):
    user_id, key = extract_data(event)

    faces = detect_faces(bucket_name, key)
    if len(faces) != 1:
        return {
            'statusCode': 400,
            "headers": {"status": "bad"},
            'body': json.dumps({"error_message": "Picture should contain only one image"})
        }

    face_id = add_face_to_collection(bucket_name, key)
    try:
        body = record_face_collection_id(user_id, face_id)
        return {
            'statusCode': 200,
            "headers": {"status": "good"},
            'body': json.dumps(body)
        }
    except Exception as e:
        return {
            'statusCode': 400,
            "headers": {"status": "bad"},
            'body': json.dumps({"error_message": str(e)})
        }
