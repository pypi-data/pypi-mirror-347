import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configure your AWS S3 bucket and region
AWS_REGION = "ap-south-1" 
S3_BUCKET_NAME = "orbitenv-dev" 

s3_client = boto3.client('s3', region_name=AWS_REGION)

def upload_file(file_path):
    """ Upload a file to AWS S3 """
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return
    
    file_name = os.path.basename(file_path) 
    
    try:
        print(f"Uploading {file_name} to S3 bucket {S3_BUCKET_NAME}...")
        s3_client.upload_file(file_path, S3_BUCKET_NAME, file_name)
        print(f"File {file_name} uploaded successfully to {S3_BUCKET_NAME}.")
    except FileNotFoundError:
        print(f"Error: {file_path} does not exist.")
    except NoCredentialsError:
        print("Error: No AWS credentials found.")
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials. Please check your setup.")
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")


def download_file(file_name):
    """ Download a file from AWS S3 """
    try:
        # Download the file from S3
        print(f"Downloading {file_name} from S3 bucket {S3_BUCKET_NAME}...")
        s3_client.download_file(S3_BUCKET_NAME, file_name, file_name)
        print(f"File {file_name} downloaded successfully.")
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
    except NoCredentialsError:
        print("Error: No AWS credentials found.")
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials. Please check your setup.")
    except Exception as e:
        print(f"Error downloading {file_name}: {e}")        