# Product rating with facial expressions

This project introduces a new, fun way to collect user feedback on a variety of products (movies, electronics, clothing, etc). The concept is to upload pictures of users' faces, expressing their reaction (happy, angry, disgusted, etc), to the cloud via a phone app. The pictures are then scanned by AWS Rekognition to detect the facial expressions and record the reactions of users to products. Using Rekognition would allow for users to collect extra characteristics about a user such as their gender and approximate age. Collecting such characteristics at one go and storing them in a data warehouse would allow for future user segmentation analysis and possibly better marketing.

## facial-reaction-parser

This AWS Lambda function is triggered when a user photo is uploaded to a specified S3 bucket. AWS Rekognition runs its face detection algorithm on the photograph, detecting the user's facial expression and inferring their gender and approximate age. This information is then passed on as a JSON string to an SNS topic.

## dynamo-db-writer

This function subscribes to the SNS topic from facial-reaction-parser. The user ID, product ID, emotion, and S3 URL for a particular Rekognition analysis are then stored in a DynamoDB table.
