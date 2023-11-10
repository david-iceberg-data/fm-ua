#%%

import json
import random
import time
from datetime import datetime
from pytz import timezone
from aux import *
import threading
import os
import requests
from retry import retry
from aux import download_blob
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor as TPE,ProcessPoolExecutor as PPE
from scratch import *

print(os.environ.get('proxy_url'))
# Define URLs
url_homescreen  = 'https://smartphone.united.com/UnitedMobileDataServicesHomeScreenNoCSG/api/HomeScreen/PutSemiPrivateClientConfig2'
url_messages    = 'https://mobiletravelapi.united.com/cceservice/api/GetPersonalizedMessages'
url_shop        = 'https://mobileshopapi.united.com/shoppingservice/api/Shopping/Shop'
url_catalog     = 'https://mobileapi.united.com/catalogservice/api/Catalog/GetCatalogItemsV2'

def get_inputs(itinerary, randomize):
    # Get inputs
    if randomize:
        #get_random_inputs
        origin,destination,departure    = get_random_inputs()
        id,Reference                    = random.randint(1,10000), random.randint(1,10000)
    else:
        origin,destination  = itinerary['originAirport'], itinerary['destinationAirport']
        departure, id       = itinerary['DepartDate']   ,itinerary['_ID']
        Reference           = itinerary['Reference']
    

    return origin, destination, departure, id, Reference

def generate_home_screen_query(deviceId_uuid, pushToken_token, transactionId_uuid, os_version, version_shop, version_ccservice):
    return {
        'deviceId': deviceId_uuid,
        'pushToken': pushToken_token,
        'data': {
            '_id': '',
            'action': 'sign_out',
            '_rev': '',
            'channels': [
                f'SP_XD913535@{deviceId_uuid}',
            ],
            'refreshIntervalInSeconds': 0,
            'eventTimestamp': round(time.time()),
            'triggeredBy': 'HandleAppUpdateEvent',
            'application': {
                'deviceId': deviceId_uuid,
                'pushToken': pushToken_token,
                'id': 1,
                'osVersion': os_version,
                'version': version_shop,
                'name': 'iOS',
                'isProduction': False,
            },
            'type': 'SemiPrivateClientConfig',
            'pnrLastNamePair': {},
        },
        'languageCode': 'en-US',
        'transactionId': transactionId_uuid,
        'application': {
            'deviceId': deviceId_uuid,
            'pushToken': pushToken_token,
            'id': 1,
            'osVersion': os_version,
            'version': version_ccservice,
            'name': 'iOS',
            'isProduction': False,
        },
        'accessCode': 'ACCESSCODE',
    }

def generate_cceservice_query(deviceId_uuid, pushToken_token, transactionId_uuid, os_version, version_ccservice, messageData):
    return {
        'data': messageData,
        'deviceId': deviceId_uuid,
        'application': {
            'deviceId': deviceId_uuid,
            'pushToken': pushToken_token,
            'id': 1,
            'osVersion': os_version,
            'version': version_ccservice,
            'name': 'iOS',
            'isProduction': False,
        },
        'languageCode': 'en-US',
        'accessCode': 'ACCESSCODE',
        'transactionId': transactionId_uuid,
    }

def generate_shop_query(deviceId_uuid, transactionId_uuid, version_shop, origin, destination, departure, travelerTypes, catalogItems):
    
    randmizebools = False
    return {
       
        'accessCode': 'ACCESSCODE',
         "numberOfSeniors": 0, # Esto aparece al final de la request "https://mobileshopapi.united.com/shoppingservice/api/Shopping/Shop"
        'isReshopChange': random.choice([True, False]) if randmizebools else False,
        'awardTravel': random.choice([True, False]) if randmizebools else False,
        'isShareTripSearchAgain': random.choice([True, False]) if randmizebools else False,
        'isEditSearchEnabledOnBookingFSR': random.choice([True, False]) if randmizebools else False,
        'trips': [
            {
                'origin': origin,
                'destination': destination,
                'useFilters': random.choice([True, False]) if randmizebools else False,
                'departDate': departure,
                'searchNearbyOriginAirports': random.choice([True, False]) if randmizebools else False,
                'destinationAllAirports': 0,
                'cabin': 'econ',
                'searchNearbyDestinationAirports': random.choice([True, False]) if randmizebools else False,
                'originAllAirports': 0,
                'changeType': '0',
            },
        ],
        'fareType': 'lf',
        'showMileageDetails': random.choice([True, False]) if randmizebools else False,
        'isELFFareDisplayAtFSR': random.choice([True, False]) if randmizebools else False,
        'hashPinCode': '',
        'searchType': 'OW',
        'isYoungAdultBooking': random.choice([True, False]) if randmizebools else False,
        'isCorporateBooking': random.choice([True, False]) if randmizebools else False,
        'numberOfChildren2To4': 0,
        'isMoneyPlusMiles': random.choice([True, False]) if randmizebools else False,
        'getNonStopFlightsOnly': random.choice([True, False]) if randmizebools else True,
        'deviceId': deviceId_uuid,
        'maxNumberOfStops': 2,
        'travelType': 'RA',
        'application': {
            'id': 1,
            'name': 'iOS',
            'isProduction': False,
            'version': version_shop,
        },
        'countryCode': 'US',
        'numberOfInfantWithSeat': 0,
        'languageCode': 'en-US',
        'maxNumberOfTrips': 25,
        'numberOfInfantOnLap': 0,
        'numberOfAdults': 0,
        'transactionId': transactionId_uuid,
        'premierStatusLevel': 0,
        'pointOfSaleCountryName': 'United States',
        'catalogItems': catalogItems,
        'numberOfChildren5To11': 0,
        'serviceType': '',
        'numberOfChildren12To17': 0,
        'experiments': [
            'NoChangeFee',
            'FSRRedesignA',
        ], # Me aparece solo: "numberOfSeniors": 0
         'travelerTypes': travelerTypes# Esto solo me aparece al principio, arriba del ACCESS CODE - Con el recuente de la cantidad por cada tipo de pasajero
    }

def get_catalog_itevsV2_query(deviceId_uuid, transactionId_uuid, version_shop):

    return {
        'deviceId': deviceId_uuid,
        'application': {
            'id': 1,
            'name': 'iOS',
            'isProduction': False,
            'version': version_shop,
        },
        'languageCode': 'en-US',
        'accessCode': 'ACCESSCODE',
        'transactionId': transactionId_uuid,
    }

def generate_auth_query(url_catalog,json_data_catalog,headers_catalog,proxy,SESSION,deviceId_uuid):
    
    res_catalog  = SESSION.post(url_catalog, json=json_data_catalog, headers=headers_catalog,proxies=proxy)
    
    items = res_catalog.json()['items']
    for _item in items:
        if _item['id'] == '10642':
            client_secret = _item['currentValue']

        if _item['id'] == '10641':
            client_secret2 =  _item['currentValue']

        if _item['id'] == '10640':
            auth_url =  _item['currentValue']

    return(json.dumps({
        "application_id": "1",
        "scope": "feedback subscribe openid",
        "grant_type": "client_credentials",
        "endUserAgentID": deviceId_uuid,
        "userType": "guest",
        "client_id": client_secret2,
        "client_secret":client_secret
    })), auth_url , SESSION

def get_shop(itinerary,unixtime_g,randomize=False):
    """Get shop results based on given itinerary and options."""
    
    # Initialize session and variables
    SESSION = requests.Session()
    process_id = os.getpid()
    thread_id =  threading.current_thread().name.replace("ThreadPoolExecutor-", "")
    
    thread_id = f'{str(process_id)}_{thread_id}'
    requires_cceservice = True
    trigger_errors = False
    flattenedFlights = None

    # Define proxy retry details

    px1,px2,px3,px4,px5 = gpx(),gpx(),gpx(),gpx(),gpx()

    retry_details = [
        # Each tuple: (proxy, timeout, cookie selector, cookie index multiplier)
        (px1, 15, 0, 1),
        (px2, 15, 1, 1),
        (px3, 20, 0, 0.6), # Base cookie from a previous position
        (px4, 20, 1, 0.6),  # Alternative cookie from a previous position
        (px5, 20, 0, 0.4), # Alternative cookie from a previous position
    ]
    #print path pwd
    print(os.getcwd())
    # Get necessary inputs
    origin, destination, departure, id, Reference               = get_inputs(itinerary, randomize)
    deviceId_uuid, pushToken_token, transactionId_uuid, X_ual   = generate_context_credentials()
    
    # Generate queries
    json_data_HomeScreen    =  generate_home_screen_query   (deviceId_uuid, pushToken_token, transactionId_uuid, os_version, version_shop, version_ccservice)
    json_data_cceservice    =  generate_cceservice_query    (deviceId_uuid, pushToken_token, transactionId_uuid, os_version, version_ccservice, messageData)
    json_data_shop          =  generate_shop_query          (deviceId_uuid, transactionId_uuid, version_shop, origin, destination, departure, travelerTypes, catalogItems)
    json_data_catalog       =  get_catalog_itevsV2_query    (deviceId_uuid, transactionId_uuid, version_shop)
    
    # Log the current search inputs
    print(f"LOG INPUT U:{unixtime_g}, T:{thread_id}, O: {origin}, D: {destination}, F: {departure}", flush=True)
    _now, start_date_time = get_now()
    
    # Retry loop for request attempts
    for attempt in range(len(retry_details)):

        proxy, timeout, arg1, arg2 = retry_details[attempt]
        
        # If errors are triggered, adjust timeout for initial attempts
        if trigger_errors and attempt < 3:
            timeout = 1
        
        try:
            # Make the API calls
            # if attempt:
            # SESSION.proxies = proxy
            res_homescreen= SESSION.post(url_homescreen, headers=headers_HomeScreen, json=json_data_HomeScreen, proxies=proxy, timeout=8 if attempt < 2 else 12)
            print("LOG ",thread_id, f"Attempt {attempt + 1}")
            
            time.sleep(random.randint(0, 30) / 10)

            if requires_cceservice:
                res_messages = SESSION.post(url_messages, headers=headers_cceservice, json=json_data_cceservice, proxies=proxy, timeout=8 if attempt < 2 else 12)
                session_id = res_messages.json()['data']['guids'][1]['id']
            
            time.sleep(random.randint(0, 50) / 10)
            
            # auth_data,auth_url,SESSION  = generate_auth_query(url_catalog,json_data_catalog,headers_catalog,proxy,SESSION,deviceId_uuid)
            # response_oauth = SESSION.post(url=auth_url, headers=headers_token, data=auth_data, proxies=proxy, timeout=8 if attempt < 2 else 12)
            headers_shop = get_headers_shop(id, X_ual, arg1, arg2)
            # headers_shop['X-acf-sensor-data'] = "3,i,Z3lXDNLW2bBAvhqbBOFZvB+VD0fx8mEbRAvh2wXhk6R1KegA2Wx/okVmREtxAB2I1NzHPmD+ZHBgd3a3NW5IgUbDZwTl/MH2jmml7HhFCiFjac7pQ1h+14RpldDUwnkOHXAlDsQ6MzajNVrxbaJ7m2pqtfeoKrWI0zARMT1WUCQ=,MkR6rX5XJHlS5papLcCEdqnv0L2FCdKBk04Jj+5Ju6pEuCA+qa7w5h9c1R2WNREkHW6TJyezzEbz0aVyBFyHwYvd2mBGzSGL59yWy0fyw3mnt18CKR6n30ayNZU7wSUnv4rPNDH95/7XRCFOUFLxqIS2PSesbGBxUa4ihQVQJA8=$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$15,7,25$$"
            response_shop = SESSION.post(url_shop, json=json_data_shop, headers=headers_shop, proxies=proxy, timeout=timeout)
            # response_shop = SESSION.post(url_shop, json=json_data_raw, headers=headers_raw, proxies=proxy, timeout=timeout)
        
        except requests.exceptions.Timeout as e:
            # print(e)
            if attempt > 5:
                # print(f"LOG ",thread_id, "Attempt " {attempt}, f" BLOCKED {e}")
                print(f"LOG  {thread_id}, Attempt : {attempt} , BLOCKED : {e}")


        flattenedFlights = validate_response(response_shop)
        # if not exists, create folder
        if not os.path.exists(f"output"):
            os.makedirs(f"output")
        
        # with open(f"output/{unixtime_g}.json", "w") as f:
        #     json.dump(response_shop.json(), f)
        # with open(f"output/{unixtime_g}_flattened.json", "w") as f:
        #     json.dump(flattenedFlights, f)

        if flattenedFlights:
            break
                
    
    # Ensure a list is returned
    if not flattenedFlights:
        flattenedFlights = []
        

    _now_2, end_date_time = get_now()
    elapsed_time_seconds = round((_now_2 - _now).total_seconds(), 2)
    result = {
        f"{origin}_{destination}_{departure}": {
            "Reference": Reference,
            "Flights": flattenedFlights
        }
    }

    print(f"LOG OUTPUT T:{thread_id}, U:{unixtime_g}, L:{len(flattenedFlights)}, R:{attempt}, O:{origin}, D:{destination}, F:{departure}, S:{start_date_time}, E:{elapsed_time_seconds}")
    return result

import functions_framework

def process_files(selected_inputs, unixtime_g, randomize=False, max_threads=30):
    """Process a list of inputs."""
    with TPE(max_workers=max_threads) as executor:
        tasks = [(input, unixtime_g, randomize) for input in selected_inputs]
        results = list(executor.map(lambda x: get_shop(*x), tasks))
    return results


def set_to_active_in_aws(file_name,unixtime_g,future_filename):
    upload_blob({"activation_timestamp":unixtime_g,
                 "future_filename":future_filename,
                 "input_filename":file_name,
                 }
                , f"Active/{file_name}.json"
                , rename=False
                )

# Already in aux script
# def delete_object(key):
#     s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
#     print(f"Deleting {key}")
#     s3.delete_object(Bucket=S3_BUCKET, Key=key)

def set_to_inactive_in_aws(file_name):
    _now = time.time()
    file_name  = f"Active/{file_name}.json"
    delete_object(f"Active/{file_name}.json", S3_BUCKET)


@functions_framework.http
def run_main(request):
    """
    Main function to run the script.
    Processes the request to either handle fixed input files or random inputs.
    """

    # Retrieve request parameters with default values
    _now_g, start_date_time_g   = get_now()
    file_name                   = request.args.get('file_name',"")
    print(f"LOG Global Processing of {file_name} at {start_date_time_g}", flush=True)
    unixtime_g                  = request.args.get('unixtime_g', str(int(time.time())))
    complement                  = request.args.get('complement', False)
    _randomize                  = int(request.args.get('r', False))
    n                           = int(request.args.get('n', 1000))
    m                           = int(request.args.get('m', 0))
    m                           = m if m < n else 0
    max_procces                 = request.args.get('max_procces', 4)
    max_threads                 = request.args.get('max_threads', 30)

    # Format filename and determine output folder
    x_file_name = file_name.replace(".csv.gz","").replace(".gz", "")
    folder      = f"output/{x_file_name}/{unixtime_g}"

    unixtime_d = str(int(time.time()))
    full_path = f"{folder}/{unixtime_d}.json"
    
    # set_to_active_in_aws(file_name,unixtime_g,full_path)
    
    # Determine number of chunks to split the input into
    chunks = max_procces

    if not _randomize:
        # Handle fixed input files
        fixed_inputfile = download_and_fix_input(file_name)

        # Option to repeat the input file if 'complement' is specified
        if complement and len(fixed_inputfile) < complement:
            fixed_inputfile = fixed_inputfile * int(complement/len(fixed_inputfile))

        selected_inputs = fixed_inputfile[m:n]
        print(f"LOG Global Processing of {file_name} at {start_date_time_g} from {m} to {n}", flush=True)

    else:
        # Handle random inputs
        print(f"LOG Global Processing at {start_date_time_g} with random inputs", flush=True)
        selected_inputs = [{} for i in range(n-m)]

    # Split selected inputs into chunks
    selected_inputs_chunks = split_into_chunks(selected_inputs, chunks)

    # Process chunks concurrently
    with PPE(max_workers=chunks) as executor:
        args_for_chunks = [(chunk, unixtime_g, _randomize, max_threads) for chunk in selected_inputs_chunks]
        futures_list = list(executor.map(process_files, *zip(*args_for_chunks)))

    # Flatten the list of results
    futures_list = [item for sublist in futures_list for item in sublist]

    # Calculate transaction metrics
    now_2_g, end_date_time_g = get_now()
    transactions_count = len(futures_list)
    elapsed_time_seconds = round((now_2_g - _now_g).total_seconds(), 2)
    TPS = round(transactions_count / int(elapsed_time_seconds), 2)
    print(f"LOG GLOBAL Transactions: {transactions_count}, Elapsed time: {elapsed_time_seconds} , TPS: {TPS}", flush=True)

    # Save results and upload

    upload_blob(futures_list, full_path)

    # Retrieve and log the list of uploaded files
    uploaded = list_directory_aws(folder+"/")

    succes_rate_list = [0]
    for _flight in futures_list:
        if len(list(_flight.values())[0]['Flights']) > 0:
            succes_rate_list.append(True)
    suceess_rate = round(sum(succes_rate_list)/len(succes_rate_list),2)

    message = {"TPS": TPS,"SR":suceess_rate, "New files": uploaded}    
    print(message, flush=True)

    delete_object(f"Active/{file_name}.json")
    list_directory_aws("Active/")

    return message


if __name__ == "__main__":
    
    # Sample run
    args = {}
    # args['file_name'] = "parallel_inputs/20231024-0215-OW-UA-stop-0359-size-4000074875/1.gz"
    # args['file_name'] = '20231024-0215-OW-UA-stop-0359-size-40000.gz'
    args['n'] = 5
    # args['m'] = 0 
    args['r'] = True
    # args['max_threads'] = 20
    # args['max_procces'] = 4
    # args['complement'] = 1000
    req = requests.Request()
    req.args = args
    run_main(req)

# %%
