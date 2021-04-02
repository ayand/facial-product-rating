import boto3
from botocore.config import Config

REGION = "us-east-2"

config = Config(
    region_name = REGION,
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

dynamodb = boto3.client('dynamodb', config=config)
rekognition = boto3.client('rekognition', config=config)
s3 = boto3.client('s3')
sns = boto3.client('sns', config=config)
ssm = boto3.client('ssm', config=config)

RATING_S3_BUCKET = # specify a globally unique name here
COLLECTION_S3_BUCKET = # specify a globally unique name here

SNS_TOPIC = "facial-rekognition-output-dev"

RATING_DYNAMODB_TABLE = "facial-reaction-parser-db-dev"
COLLECTION_DYNAMODB_TABLE = "user-facial-collection-dev"

FACIAL_RATING_COLLECTION = "facial-rating-collection"

# Set up S3 buckets; leave out CreateBucketConfiguration if REGION = 'us-east-1'

s3_response_1 = s3.create_bucket(
    ACL="public-read-write",
    Bucket=RATING_S3_BUCKET,
    CreateBucketConfiguration={
        'LocationConstraint': REGION
    }
)
print("Status Code for Rating Bucket Creation")
print(s3_response_1['ResponseMetadata']['HTTPStatusCode'])
print("\n")

ssm_response_1 = ssm.put_parameter(
    Name="/FacialProductRating/RATING_S3_BUCKET",
    Value=RATING_S3_BUCKET,
    Type="String"
)
print("Status Code for RATING_S3_BUCKET")
print(ssm_response_1['ResponseMetadata']['HTTPStatusCode'])
print("\n")

s3_response_2 = s3.create_bucket(
    ACL="public-read-write",
    Bucket=COLLECTION_S3_BUCKET,
    CreateBucketConfiguration={
        'LocationConstraint': REGION
    }
)
print("Status Code for Rating Bucket Creation")
print(s3_response_2['ResponseMetadata']['HTTPStatusCode'])
print("\n")

ssm_response_2 = ssm.put_parameter(
    Name="/FacialProductRating/COLLECTION_S3_BUCKET",
    Value=COLLECTION_S3_BUCKET,
    Type="String"
)
print("Status Code for COLLECTION_S3_BUCKET")
print(ssm_response_2['ResponseMetadata']['HTTPStatusCode'])
print("\n")

# Set up SNS

sns_response = sns.create_topic(
    Name=SNS_TOPIC
)
print("Status Code for SNS Topic")
print(sns_response['ResponseMetadata']['HTTPStatusCode'])
print("\n")

SNS_ARN = sns_response['TopicArn']

ssm_response_3 = ssm.put_parameter(
    Name="/FacialProductRating/SNS_ARN",
    Value=SNS_ARN,
    Type="String"
)
print("Status Code for SNS_ARN")
print(ssm_response_3['ResponseMetadata']['HTTPStatusCode'])
print("\n")

# Set up DynamoDB

dynamodb_response_1 = dynamodb.create_table(
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        },
    ],
    TableName=RATING_DYNAMODB_TABLE,
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        }
    ],
    BillingMode="PAY_PER_REQUEST"
)
print("Status Code for DynamoDB Table 1")
print(dynamodb_response_1['ResponseMetadata']['HTTPStatusCode'])
print("\n")

ssm_response_4 = ssm.put_parameter(
    Name="/FacialProductRating/RATING_DYNAMODB_TABLE",
    Value=RATING_DYNAMODB_TABLE,
    Type="String"
)
print("Status Code for RATING_DYNAMODB_TABLE")
print(ssm_response_4['ResponseMetadata']['HTTPStatusCode'])
print("\n")

dynamodb_response_2 = dynamodb.create_table(
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        },
    ],
    TableName=COLLECTION_DYNAMODB_TABLE,
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        }
    ],
    BillingMode="PAY_PER_REQUEST"
)
print("Status Code for DynamoDB Table 2")
print(dynamodb_response_2['ResponseMetadata']['HTTPStatusCode'])
print("\n")

ssm_response_5 = ssm.put_parameter(
    Name="/FacialProductRating/COLLECTION_DYNAMODB_TABLE",
    Value=COLLECTION_DYNAMODB_TABLE,
    Type="String"
)
print("Status Code for COLLECTION_DYNAMODB_TABLE")
print(ssm_response_5['ResponseMetadata']['HTTPStatusCode'])
print("\n")

# Set up Rekognition

rekognition_response = rekognition.create_collection(CollectionId=FACIAL_RATING_COLLECTION)
print("Status Code for Rekognition Collection creation")
print(rekognition_response['ResponseMetadata']['HTTPStatusCode'])
print("\n")

ssm_response_6 = ssm.put_parameter(
    Name="/FacialProductRating/FACIAL_RATING_COLLECTION",
    Value=FACIAL_RATING_COLLECTION,
    Type="String"
)
print("Status Code for FACIAL_RATING_COLLECTION")
print(ssm_response_6['ResponseMetadata']['HTTPStatusCode'])
print("\n")
