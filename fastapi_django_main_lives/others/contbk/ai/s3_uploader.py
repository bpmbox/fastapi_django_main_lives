import boto3
from botocore.exceptions import NoCredentialsError

class S3Uploader:
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3', aws_access_key_id=self.aws_access_key_id,
                              aws_secret_access_key=self.aws_secret_access_key)

    def upload_file(self, file_path, key):
        try:
            self.s3.upload_file(file_path, self.bucket_name, key)
            print(f"Uploaded {file_path} to S3 as {key}")
        except NoCredentialsError:
            print("Credentials not available")