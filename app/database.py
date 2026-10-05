import boto3


dynamodb = boto3.resource(
    "dynamodb",
    region_name="eu-west-2"
)

table = dynamodb.Table("job-applications")