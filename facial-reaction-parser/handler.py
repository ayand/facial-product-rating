import json
import boto3
import time
import os
from datetime import datetime

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')
sns = boto3.client('sns')

def analyze_face(bucket, key):
    facial_analysis = rekognition.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':key}},Attributes=['ALL'])
    face = facial_analysis["FaceDetails"][0]

    emotions = sorted(face["Emotions"], key=lambda x: x["Confidence"], reverse=True)
    primary_emotion = emotions[0]['Type']
    gender = face["Gender"]["Value"]
    approx_age = (face["AgeRange"]["Low"] + face["AgeRange"]["High"]) / 2
    return (primary_emotion, gender, approx_age,)

def get_product_and_user(key):
    # Format of key: products/<product-id>/ratings/rating_user_<user-id>.jpg
    components = key.split("/")
    product_id = components[-3]
    user_id = components[-1].replace(".jpg", "").split("_")[2]
    return (product_id, user_id,)

def build_data_point(product_id, user_id, emotion, gender, age, url):
    body = {
        "id": product_id + "_" + user_id,
        "productId": product_id,
        "userId": user_id,
        "emotion": emotion,
        "gender": gender,
        "age": age,
        "url": url,
        "timestamp": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    }
    return body

def handler(event, context):
    """ Parse newly created objects and analyze a face for emotion, gender, and age """
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    product_id, user_id = get_product_and_user(key)

    emotion, gender, age = analyze_face(bucket, key)

    url = '{}/{}/{}'.format(s3.meta.endpoint_url, bucket, key)

    body = build_data_point(product_id, user_id, emotion, gender, age, url)

    sns_response = sns.publish(TopicArn=os.environ['SNS_TOPIC_ARN'], Message=json.dumps(body))

    return sns_response
