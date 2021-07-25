import boto3
from botocore.config import Config

REGION = "us-east-1"

config = Config(
    region_name = REGION,
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

rekognition = boto3.client('rekognition', config=config)
ssm = boto3.client('ssm', config=config)

FACIAL_RATING_COLLECTION = "facial-rating-collection"

# Set up Rekognition
rekognition_response = rekognition.create_collection(CollectionId=FACIAL_RATING_COLLECTION)
print("Status Code for Rekognition Collection creation")
print(rekognition_response['ResponseMetadata']['HTTPStatusCode'])
print("\n")

ssm_response = ssm.put_parameter(
    Name="/FacialProductRating/FACIAL_RATING_COLLECTION",
    Value=FACIAL_RATING_COLLECTION,
    Type="String"
)
print("Status Code for FACIAL_RATING_COLLECTION")
print(ssm_response['ResponseMetadata']['HTTPStatusCode'])
print("\n")
