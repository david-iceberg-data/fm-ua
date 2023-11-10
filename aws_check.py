#%%
import boto3
import gzip
import json
from aux import S3_BUCKET as bucket_name,aws_access_key, aws_secret_key,down



def download_blob(name_file_to_save,name_file_to_dwld ):
    # Specify the name of your S3 bucket and object key
    s3_bucket_name = bucket_name
    s3_object_key = name_file_to_dwld # Replace with the desired object key

    # Create an S3 client
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

    try:
        # Download the .gz file from S3
        response = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_object_key)
        gzipped_data = response['Body'].read()

        # Extract the contents from the gzipped file
        file_contents = gzip.decompress(gzipped_data).decode('utf-8')

        # Save the file locally
        with open(f'{name_file_to_save}', 'w') as file:
            file.write(file_contents)

        # convert in json
        file_contents = json.loads(file_contents)
        print("File downloaded and extracted successfully!")
        return file_contents
        #return "File downloaded and extracted successfully!"
    except Exception as e:
        print("Error:", str(e))
        return f"Error: {str(e)}"

def list_directory_aws(prefix):
               
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        all_objects = []

        # Use paginator to handle the case when there are more than 1000 objects in the bucket
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name
                                    #    ,Prefix=prefix
                                       ):
            for obj in page.get('Contents', []):
                all_objects.append(obj['Key'])

        return all_objects

list_directory_aws("")
#%%
# download_blob(name_file_to_save="50.json"
#               ,name_file_to_dwld="20231018-0102-RT-UA-stop-0246-size-50.csv.gz"
#               )


download_blob(name_file_to_save="50.json"
              ,name_file_to_dwld="20231018-0102-RT-UA-stop-0246-size-50.gz"
              )
#%%
from aux import upload_blob

upload_blob("20231020-1940-RT-UA-stop-2124-size-1000.json")
# upload_blob("20231018-0102-RT-UA-stop-0246-size-50.json")

