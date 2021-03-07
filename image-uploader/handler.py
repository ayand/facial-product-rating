import boto3
import json
import base64
import os

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
bucket_name = os.environ['S3_BUCKET']

def extract_data(event):
    body = json.loads(event['body'])

    user_id = event['pathParameters']['userId']
    product_id = body['productId']
    image_data = body['image_data']

    return (user_id, product_id, image_data)

def upload_image(user_id, product_id, image_data):
    key = "products/{}/ratings/rating_user_{}.jpg".format(product_id, user_id)
    object = s3.Object(bucket_name, key)
    object.put(Body=base64.b64decode(image_data))
    url = '{}/{}/{}'.format(s3_client.meta.endpoint_url, bucket_name, key)
    return url


def handler(event, context):
    try:
        user_id, product_id, image_data = extract_data(event)
        url = upload_image(user_id, product_id, image_data)

        output = {
            "user_id": user_id,
            "product_id": product_id,
            "image_url": url
        }

        return {
            'statusCode': 200,
            "headers": {"status": "good"},
            'body': json.dumps(output)
        }
    except Exception as e:
        return {

            'statusCode': 500,
            "headers": {"status": "bad"},
            'body': json.dumps({"error_message": str(e)})
        }
