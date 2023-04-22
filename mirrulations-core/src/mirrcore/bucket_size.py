from datetime import datetime, timedelta
import os
import boto3
from dotenv import load_dotenv
import math

end_time = datetime.utcnow()
start_time = end_time - timedelta(days=2)


class BucketSize:
    """
    A class which handles getting the size of the mirrulations bucket
    on S3

    Uses cloudwatch client
    ...
    Methods
    -------
    get_bucket_size()
    """

    @staticmethod
    def get_bucket_size():
        """Returns the size of the bucket in gigabytes"""
        client = BucketSize.get_client()
        result = client.get_metric_statistics(
            Namespace="AWS/S3",
            Dimensions=[{"Name": "BucketName", "Value": "mirrulations"},
                        {"Name": "StorageType", "Value": "StandardStorage"}],
            MetricName="BucketSizeBytes",
            StartTime=start_time,
            EndTime=datetime.utcnow(),
            Period=86400,  # 1 day in seconds
            Statistics=['Average'],
            Unit='Bytes'
        )
        # Extract the bucket size from the client metric data
        bucket_size_bytes = result['Datapoints'][0]["Average"]

        # Convert the size from bytes to GB
        bucket_size_gb = math.ceil(bucket_size_bytes / (1024 ** 3))

        return bucket_size_gb

    @staticmethod
    def get_client():
        """
        Returns a cloudwatch client connection
        """
        access_key, secret_access_key = BucketSize.get_credentials()

        if access_key is None or secret_access_key is None:
            print("No AWS credentials provided, Unable to write to S3.")
            return False
        return boto3.client(
                    "cloudwatch",
                    region_name='us-east-1',
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_access_key
                    )

    @staticmethod
    def get_credentials():
        """
        Loads aws credentials from .env file
        Saves credentials to instance variables
        """
        load_dotenv()
        access_key = os.getenv("AWS_ACCESS_KEY")
        secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        return [access_key, secret_access_key]
