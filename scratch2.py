#%%
import requests

headers = {
    'Host': 'mobileshopapi.united.com',
    'Connection': 'keep-alive',
    'X-acf-sensor-data': '3,i,AYETREbh0mKqu6xDYtWYFX5cMDVHQXivvLTe+FqpxGKiPd1G7jH9hFAh0s0iukjD4/+y+5s2H5mmf5qXxL9mZeaXF0YOJ2MaxBPKbkYY9dhPhiU1xF7taAhmFxKE3Vzx74+MnmwylEhbbfos57GH5irQwDqlEZ+Tam/5EX5ZWAA=,q1oxbc2mhGZMcPISVAY3444BcpbHdu0kzsXbILMe9Tb55YJIm7kEaBIkZYOVJZ0iRkSjKljIX52rTZrUJzO4M+AJDldi+BH2g6QBOla7gXF/iV0ZgmVqazX5kj1ov0epOHHFWQBxlzRMSXrtPswYXOxQDde+qfcJsZUCzCT2I5c=$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$20,9,23$$',
    'X-Ual': '14EE7EE8-1FE9-41EF-8958-5486C0092E5F',
    'Accept': '*/*',
    'User-Agent': 'UnitedCustomerFacingIPhone/4.1.93 (Version 15.7 (Build 21G419))',
    'Accept-Language': 'en-US,en;q=0.9',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json',
}

json_data = {
    'accessCode': 'ACCESSCODE',
    'travelerTypes': [
        {
            'count': 2,
            'travelerType': 'Adult',
        },
        {
            'count': 0,
            'travelerType': 'Senior',
        },
        {
            'count': 0,
            'travelerType': 'Child15To17',
        },
        {
            'count': 0,
            'travelerType': 'Child12To14',
        },
        {
            'count': 0,
            'travelerType': 'Child5To11',
        },
        {
            'count': 0,
            'travelerType': 'Child2To4',
        },
        {
            'count': 0,
            'travelerType': 'InfantSeat',
        },
        {
            'count': 0,
            'travelerType': 'InfantLap',
        },
    ],
    'isReshopChange': False,
    'experiments': [
        'NoChangeFee',
        'FSRRedesignA',
    ],
    'awardTravel': False,
    'isShareTripSearchAgain': False,
    'isEditSearchEnabledOnBookingFSR': False,
    'resultSortType': '',
    'showMileageDetails': False,
    'fareType': 'LF',
    'trips': [
        {
            'origin': 'ATL',
            'destination': 'IAD',
            'useFilters': False,
            'shareMessage': '',
            'searchNearbyOriginAirports': False,
            'departDate': '11/30/2023',
            'destinationAllAirports': 0,
            'cabin': 'econ',
            'searchNearbyDestinationAirports': False,
            'originAllAirports': 0,
            'changeType': '0',
        },
    ],
    'cameFromFSRHandler': False,
    'isELFFareDisplayAtFSR': False,
    'hashPinCode': '',
    'searchType': 'OW',
    'isYoungAdultBooking': False,
    'isCorporateBooking': False,
    'fareClass': '',
    'numberOfChildren2To4': 0,
    'isMoneyPlusMiles': False,
    'getNonStopFlightsOnly': False,
    'bwcsessionId': '',
    'deviceId': '8FEFAAC2-3F0E-55AA-A9C3-368EFDDB015C',
    'lengthOfCalendar': 0,
    'maxNumberOfStops': 2,
    'travelType': 'RA',
    'employeeDiscountId': '',
    'application': {
        'id': 1,
        'name': 'iOS',
        'isProduction': False,
        'version': {
            'minor': '4.1.93',
            'major': '4.1.93',
            'displayText': '',
            'build': '',
        },
    },
    'countryCode': 'US',
    'numberOfInfantWithSeat': 0,
    'columnFareType': '',
    'promotionCode': '',
    'languageCode': 'en-US',
    'maxNumberOfTrips': 25,
    'numberOfInfantOnLap': 0,
    'numberOfAdults': 0,
    'transactionId': '8FEFAAC2-3F0E-55AA-A9C3-368EFDDB015C|8BD689D4-931E-4411-9F7E-0D40FD61B8BC',
    'premierStatusLevel': 0,
    'pointOfSaleCountryName': 'United States',
    'catalogItems': [
        {
            'id': '11388',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '11389',
            'saveToPersist': False,
            'currentValue': '0',
        },
        {
            'id': '11428',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '11587',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '11502',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '11699',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '11647',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '11643',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '11757',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '11870',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '12125',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '11793',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '11815',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '11867',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '11873',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '11890',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '12003',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '11878',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '11936',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '12061',
            'saveToPersist': False,
            'currentValue': '0',
        },
        {
            'id': '12122',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '12106',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '12093',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '12121',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '12208',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '12178',
            'saveToPersist': False,
            'currentValue': '',
        },
        {
            'id': '12221',
            'saveToPersist': False,
            'currentValue': '1',
        },
        {
            'id': '12283',
            'saveToPersist': False,
            'currentValue': '1',
        },
    ],
    'numberOfChildren5To11': 0,
    'serviceType': '',
    'numberOfChildren12To17': 0,
    'sessionId': '39595C1DEA864F84A7084A3ED59F39FB',
    'isExpertModeEnabled': False,
    'getFlightsWithStops': True,
    'numberOfSeniors': 0#, borrar coma
}

response = requests.post(
    'https://mobileshopapi.united.com/shoppingservice/api/Shopping/Shop',
    headers=headers,
    json=json_data,
    verify=False,
)
response.json()
