import boto3

rekognition = boto3.client('rekognition')
collection_id = "facial-rating-collection"
rekognition_response = rekognition.create_collection(CollectionId=collection_id)

print(rekognition_response['CollectionArn'])

ssm = boto3.client('ssm')

ssm_response = ssm.put_parameter(
    Name="/FacialProductRating/FACIAL_RATING_COLLECTION",
    Value=collection_id,
    Type="String"
)

print(ssm_response['ResponseMetadata']['HTTPStatusCode'])
