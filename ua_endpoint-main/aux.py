#%%
import hashlib
import requests
import uuid
import random
from math import ceil
from pytz import timezone
import gzip
import boto3
import os
import json
from datetime import datetime
import time
from dotenv import load_dotenv
import csv


app_version = '4.1.93'
# os_version = '15.7'
# build_version = '21G419'
os_version = '15.5'
build_version = '19F77'

HEADERS = "https://storage.googleapis.com/crackers_store/headers_old.csv"
S3_BUCKET = "3v-iceberg-dev"

def load_enviroment_variables():
    """ Load environment variables from .env file. """
    load_dotenv()

    # Load environment variables
    global gpx_username
    global gpx_password
    global aws_access_key
    global aws_secret_key
    global proxy_url
    global proxy_port

    gpx_username = os.getenv("gpx_username")
    gpx_password = os.getenv("gpx_password")
    aws_access_key = os.getenv("aws_access_key")
    aws_secret_key = os.getenv("aws_secret_key")
    proxy_url = os.getenv("proxy_url")
    proxy_port = os.getenv("proxy_port")

load_enviroment_variables()

def list_directory_aws(prefix = ""):

        bucket_name = S3_BUCKET
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        all_objects = []

        # Use paginator to handle the case when there are more than 1000 objects in the bucket
        paginator = s3_client.get_paginator('list_objects_v2')

        if prefix == "":
                for page in paginator.paginate(Bucket=bucket_name
                                       ):
                    for obj in page.get('Contents', []):
                        all_objects.append(obj['Key'])
        else:
            for page in paginator.paginate(Bucket=bucket_name
                                        ,Prefix=prefix
                                        ):
                for obj in page.get('Contents', []):
                    all_objects.append(obj['Key'])

        return all_objects


# Global data
def delete_object(key):
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    print(f"Deleting {key}")
    s3.delete_object(Bucket=S3_BUCKET, Key=key)

def load_crackers_data():
    """ Load CSV data into global variable once. """
    response = requests.get(HEADERS)
    f = response.text.splitlines()  # Convert the string response to a list of lines
    reader = csv.DictReader(f)
    
    crackers_data = []
    for row in reader:
        crackers_data.append(row)
    print("Loaded crackers data from gcs.")
    return crackers_data

global crackers_data
crackers_data = load_crackers_data()
global crackers_data_len
crackers_data_len = len(crackers_data)


# Specify your AWS access key and secret key
user_agent = f'UnitedCustomerFacingIPhone/{app_version} (Version {os_version} (Build {build_version}))'
# user_agent = 'UnitedCustomerFacingIPhone/4.1.92.6 CFNetwork/1335.0.3.1 Darwin/21.6.0'

version_shop = {
                'minor': app_version,
                'major': app_version,
                'displayText': '',
                'build': '',
            }

version_ccservice = {
                'minor': app_version[2],
                'major': app_version[0],
                'displayText': '',
                'build': app_version[4:],
            }

def gpx():

    port = int(proxy_port)
    session_id = random.random()

    if proxy_url.startswith('brd'):
        super_proxy_url = ('http://%s-session-%s:%s@%s:%d' %
        (gpx_username, session_id, gpx_password, proxy_url,port))
    else:
        super_proxy_url = ('http://customer-%s:%s@%s:%d' %
        (gpx_username, gpx_password, proxy_url,port))
    # print (super_proxy_url)
    proxy_handler ={
        'http': super_proxy_url,
        'https': super_proxy_url,
    }

    return proxy_handler

def get_cracker_data_online(id):
    ce = f"https://us-central1-iceberg-data.cloudfunctions.net/testing3victors?search={id}"
    try:
        res = requests.get(ce)
        res.raise_for_status()  # Raise an exception for any HTTP errors (e.g., 404, 500)
        data = res.json().get("data", {}).get("crackers", [])
        if len(data) > 1:
            return data[0] ,data[1]
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def get_headers_shop(id,X_ual,selection=0,multiplier = 1):

    input_id = id * multiplier
    #round up to 0 decimals and conver to no dcimals
    input_id = int(ceil(input_id))    

    headers_shop={
        "Host": "mobileshopapi.united.com",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        'X-acf-sensor-data': get_cracker_data(int(input_id))[selection],
        'X-Ual': X_ual,
        'Accept': '*/*',
        'User-Agent': user_agent,
        'Accept-Language': 'en-US,en;q=0.9',
        "Accept-Encoding": "gzip, deflate, br",
        # 'Pragma': 'no-cache',
        # 'Cache-Control': 'no-cache',
        # 'Content-Type': 'application/json',
    }

    
    return headers_shop

def get_random_inputs():
    airports = ["JFK", "LAX", "ORD", "DFW", "DEN", "IAH", "ATL", "PHX", "SFO", "LAS"]
    origin = random.choice(airports)
    airports.remove(origin)
    destination = random.choice(airports)
    departure = f"{random.randint(1,12)}/{random.randint(1,28)}/2024"
    return origin,destination,departure

def generate_sha256_hash(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()
    
headers_HomeScreen = {
        'Host': 'smartphone.united.com',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': user_agent,
        'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
    }

headers_catalog = {
    'Host': 'mobileapi.united.com',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'User-Agent': 'UnitedCustomerFacingIPhone/4.1.92.6 CFNetwork/1335.0.3.1 Darwin/21.6.0',
    'Accept-Language': 'en-US,en;q=0.9',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json',
}

headers_cceservice = headers_HomeScreen.copy()

headers_cceservice['Host'] = 'mobiletravelapi.united.com'

def generate_context_credentials():
    deviceId_uuid = uuid.uuid4()
    deviceId_uuid = str(deviceId_uuid).upper()

    input_data = deviceId_uuid
    pushToken_token = generate_sha256_hash(input_data)

    transactionId_uuid = uuid.uuid4()
    transactionId_uuid = str(transactionId_uuid).upper()
    transactionId_uuid = f'{deviceId_uuid}|{transactionId_uuid}'

    X_ual= uuid.uuid4()
    X_ual = str(X_ual).upper()

    return deviceId_uuid, pushToken_token, transactionId_uuid , X_ual

def validate_response(response_shop):
    return(response_shop.json()['availability']['trip']['flattenedFlights'])

travelerTypes = [
    {
      "count": 2,
      "travelerType": "Adult"
    },
    {
      "count": 0,
      "travelerType": "Senior"
    },
    {
      "count": 0,
      "travelerType": "Child15To17"
    },
    {
      "count": 0,
      "travelerType": "Child12To14"
    },
    {
      "count": 0,
      "travelerType": "Child5To11"
    },
    {
      "count": 0,
      "travelerType": "Child2To4"
    },
    {
      "count": 0,
      "travelerType": "InfantSeat"
    },
    {
      "count": 0,
      "travelerType": "InfantLap"
    }
  ]

catalogItems = [
            {
                'id': '11388',
                'currentValue': '1',
            },
            {
                'id': '11389',
                'currentValue': '0',
            },
            {
                'id': '11428',
                'currentValue': '1',
            },
            {
                'id': '11587',
                'currentValue': '1',
            },
            {
                'id': '11502',
                'currentValue': '1',
            },
            {
                'id': '11699',
                'currentValue': '1',
            },
            {
                'id': '11647',
                'currentValue': '1',
            },
            {
                'id': '11643',
                'currentValue': '1',
            },
            {
                'id': '11757',
                'currentValue': '1',
            },
            {
                'id': '11870',
                'currentValue': '1',
            },
            {
                'id': '12125',
                'currentValue': '1',
            },
            {
                'id': '11793',
                'currentValue': '1',
            },
            {
                'id': '11815',
                'currentValue': '1',
            },
            {
                'id': '11867',
                'currentValue': '1',
            },
            {
                'id': '11873',
                'currentValue': '1',
            },
            {
                'id': '11890',
                'currentValue': '1',
            },
            {
                'id': '12003',
                'currentValue': '1',
            },
            {
                'id': '11878',
                'currentValue': '1',
            },
            {
                'id': '11936',
                'currentValue': '1',
            },
            {
                'id': '12061',
                'currentValue': '1',
            },
            {
                'id': '12122',
                'currentValue': '1',
            },
            {
                'id': '12106',
                'currentValue': '1',
            },
            {
                'id': '12093',
                'currentValue': '1',
            },
            {
                'id': '12121',
                'currentValue': '1',
            },
            {
                'id': '12208',
                'currentValue': '1',
            },
            {
                'id': '12178',
                'currentValue': '',
            },
            {
                'id': '12221',
                'currentValue': '1',
            },
            {
                "id": "12283",
                "currentValue": "1"
            }
        ]

messageData = {
            'requestor': {},
            'langCode': 'en',
            'caCardPNR': '',
            'channelType': 'MOB',
            'validationParameters': {
                'LASTNAME': '',
                'TOKEN': 'J42+5ucYF9mYi7ylXxRBw4/DZK1KGFflZ5vSX0zSQ4xHJl68rxoSmNtgj5EiA8AMa0U1Ycz/HwBHB8q6yUGUYaYvktQb0rvQnoV/GjDSfGtoftz/M5IYJ/LVdLg/1jPIksz7AbgAP5yGuovSaI/Izw==',
                'MPNUMBER': '',
                'RESERVATION': '',
                'HASH': '',
            },
            'geoLocation': {
                'longitude': '',
                'latitude': '',
            },
            'caCardType': '0',
            'IPCountry': 'us',
            'componentsToLoad': [
                'HeroMsg',
                'PuwyloCarousel',
                'GenericCarousel',
                'HeroCenter',
                'OmniCartIndicator',
                'TravelPlanner',
                'ChaseBannerHomepage',
                'ChaseBannerMP',
                'ChaseBannerPDE',
                'ChaseBannerBP',
                'ChaseBannerWAL1',
                'ChaseBannerFCI',
                'ChaseBannerMP2',
                'TopOffer',
            ],
            'grpPnrTravelers': [],
            'mileagePlusId': '',
            'pageToLoad': 'Homepage',
            'isCloudCACard': False,
        }

def download_blob(name_file_to_save,name_file_to_dwld ):
    # Specify the name of your S3 bucket and object key
    s3_bucket_name = "3v-dev-iceberg"
    s3_object_key = name_file_to_dwld # Replace with the desired object key

    # Create an S3 client
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

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



def convert_date(date_str):
    # Convert to a datetime object using strptime
    date_obj = datetime.strptime(date_str, "%Y%m%d")

    # Format the datetime object back to a string using strftime
    formatted_date_str = date_obj.strftime("%Y/%-m/%-d")

    return(formatted_date_str)

def loop_index(total_intems,max_amount_of_items):
    return total_intems%max_amount_of_items

def fix_inputfile(inputfile):
    new_inputfile = []
    I = 0
    J = loop_index(I,crackers_data_len)
    #create random list of n numbers between 1 and 10000
    cracker_index=list(range(1, crackers_data_len))
    random.shuffle(cracker_index) 

    for itinerary in inputfile:
        originAirport           = itinerary['originAirport']
        destinationAirport      = itinerary['destinationAirport']
        DepartDate              = convert_date(itinerary['DepartDate'])
        Reference               = itinerary['Reference']
        _ID                     = cracker_index[J]
        I                       =I+1
        fixed_input = {"originAirport":originAirport,"destinationAirport":destinationAirport,"DepartDate":DepartDate,"_ID":_ID,"Reference":Reference}
        new_inputfile.append(fixed_input)

    return(new_inputfile)

def upload_blob_from_file(name_json):

    # Specify the name of your S3 bucket and object key
    s3_bucket_name = "3v-dev-iceberg"
    with open(f"{name_json}", 'r') as file:
        data = json.load(file)    

    name_json= str(name_json).replace('json','gz')
    s3_object_key = f"{name_json}"   

    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

    gcs_data = json.dumps(data)

    # Upload the compressed data to S3
    s3_client.put_object(
        Bucket=s3_bucket_name,
        Key=s3_object_key,
        Body=gzip.compress(gcs_data.encode('utf-8'))
    )

    print("uploaded file: ", name_json)
    
def upload_blob(Json_to_upload,name_json , rename=True):

    data = Json_to_upload
    s3_bucket_name = S3_BUCKET

    # name_json= str(name_json).replace('json','json.gz')
    #only replace the extension if it ends with .json
    if name_json.endswith('.json') and rename:
        name_json = name_json[:-5] + '.json.gz'

    s3_object_key = f"{name_json}"   

    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

    gcs_data = json.dumps(data)

    # Upload the compressed data to S3
    s3_client.put_object(
        Bucket=s3_bucket_name,
        Key=s3_object_key,
        Body=gzip.compress(gcs_data.encode('utf-8'))
    )

    print("uploaded file: ", name_json)
def list_directory_aws(prefix):

        bucket_name = S3_BUCKET
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
        all_objects = []

        # Use paginator to handle the case when there are more than 1000 objects in the bucket
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name,Prefix=prefix):
            for obj in page.get('Contents', []):
                all_objects.append(obj['Key'])

        return all_objects

def get_now():
        time_zone = 'America/Bogota'
        now_dt = datetime.now(timezone(time_zone))
        now_text = now_dt.strftime("%m/%d/%Y, H:%H:%M:%S")
        return now_dt, now_text

def download_and_fix_input(file_name):
    """Download and fix input file."""
    inputfile = download_blob("input.json", file_name)

    random.shuffle(inputfile)
    return fix_inputfile(inputfile)


def save_to_output_folder(folder, data):
    """Save processed data to the output folder."""
    os.makedirs(folder, exist_ok=True)
    unixtime_d = str(int(time.time()))
    filename = f"{folder}/{unixtime_d}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    return filename



def get_data_by_id(id_):
    total_rows = len(crackers_data)
    threshold_80 = int(total_rows * 0.8)

    # Adjust indices based on DataFrame lengths.
    id_df1 = id_ % threshold_80  # equivalent to repeated subtraction
    id_df2 = id_ % (total_rows - threshold_80)
    id_df2 = threshold_80 + id_df2

    # Extract rows based on computed indices.
    df_1_row = crackers_data[id_df1]
    df_2_row = crackers_data[id_df2]

    # Prepare response.
    resp = {
        'crackers': (df_1_row['cracker'], df_2_row['cracker']),
        'last_date': max(df_1_row['timestamp'], df_2_row['timestamp']),
        'input': str(id_),
        'total_rows': str(total_rows),
        'threshold_80': str(threshold_80),
        'id_df1': str(id_df1),
        'id_df2': str(id_df2),
    }
    return resp


def get_cracker_data(id_):   
    try: 
        data = get_data_by_id(id_).get("crackers", [])
        return data[0] ,data[1]
    except Exception as e:
        print(f"An error occurred: {e}")
        # return get_cracker_data_online(id_)

def split_into_chunks(lst, num_chunks):
    """Split a list into a specified number of chunks."""
    avg = len(lst) / float(num_chunks)
    out = []
    last = 0.0

    while last < len(lst):
        out.append(lst[int(last):int(last + avg)])
        last += avg

    return out

headers_token = {
                    "Host": "aws.prdgw.api.united.com",
                    "Content-Type": "application/json",
                    "Connection": "keep-alive",
                    "Accept": "*/*",
                    "User-Agent": user_agent,
                    "Content-Length": "283",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                    }