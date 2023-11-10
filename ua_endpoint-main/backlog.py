def generate_farewall_query(deviceId_uuid, transactionId_uuid, version_ccservice, origin, destination, departure, travelerTypes, catalogItems): 
  import random
  return {
  "accessCode": "ACCESSCODE",
  "travelerTypes": travelerTypes,
  "isReshopChange": random.choice([True, False]),
  "experiments": [
    "NoChangeFee",
    "FSRRedesignA"
  ],
  "awardTravel": random.choice([True, False]),
  "isShareTripSearchAgain": random.choice([True, False]),
  "isEditSearchEnabledOnBookingFSR": random.choice([True, False]),
  "resultSortType": "",
  "showMileageDetails": random.choice([True, False]),
  "fareType": "LF",
  "trips": [
    {
      "shareMessage": "",
      "cabin": "econ",
      "useFilters": False,
      "searchFiltersIn": {
        "showDurationFilters": False,
        "carrierExpress": False,
        "showSortingandFilters": False,
        "bookingCodes": "",
        "timeArrivalMax": "",
        "durationMax": 0,
        "fareFamily": "",
        "carriersOperating": "",
        "priceMin": 0,
        "showRefundableFaresToggle": False,
        "priceMax": 0,
        "carrierPartners": False,
        "showLayOverFilters": False,
        "airportsDestination": "",
        "durationStopMax": 0,
        "airportsStopToAvoid": "",
        "equipmentTypes": "",
        "filterSortPaging": False,
        "airportsOrigin": "",
        "showPriceFilters": False,
        "priceMinDisplayValue": "",
        "sortType1": "",
        "durationStopMin": 0,
        "cabinCountMin": 0,
        "carrierDefault": False,
        "carrierStar": False,
        "stopCountExcl": 0,
        "showDepartureFilters": False,
        "showArrivalFilters": False,
        "airportsStop": "",
        "cabinCountMax": 0,
        "aircraftTypes": "",
        "priceMaxDisplayValue": "",
        "equipmentCodes": "",
        "pageNumber": 0,
        "carriersMarketing": "",
        "timeDepartMin": "",
        "stopCountMin": 0,
        "refundableFaresToggle": {
          "amount": "",
          "value": "Refundable Fares",
          "key": "RefundableFares",
          "displayValue": "Refundable fares from $234",
          "currency": "",
          "isSelected": False
        },
        "timeDepartMax": "",
        "stopCountMax": 0,
        "durationMin": 0,
        "timeArrivalMin": ""
      },
      "searchNearbyDestinationAirports": False,
      "searchNearbyOriginAirports": False,
      "destinationAllAirports": 0,
      "changeType": "0",
      "departDate": departure,
      "origin":  origin,
      "destination": destination,
      "originAllAirports": 0
    }
  ],
  "cameFromFSRHandler": False,
  "isELFFareDisplayAtFSR": False,
  "hashPinCode": "",
  "searchType": "OW",
  "isYoungAdultBooking": False,
  "isCorporateBooking": False,
  "fareClass": "",
  "numberOfChildren2To4": 0,
  "isMoneyPlusMiles": False,
  "getNonStopFlightsOnly": False,
  "bwcsessionId": "",
  "deviceId": deviceId_uuid,
  "lengthOfCalendar": 0,
  "maxNumberOfStops": 2,
  "travelType": "RA",
  "employeeDiscountId": "",
  "application": {
    "id": 1,
    "name": "iOS",
    "isProduction": False,
    "version": version_ccservice
  },
  "countryCode": "US",
  "numberOfInfantWithSeat": 0,
  "columnFareType": "",
  "promotionCode": "",
  "languageCode": "en-US",
  "maxNumberOfTrips": 25,
  "numberOfInfantOnLap": 0,
  "numberOfAdults": 0,
  "transactionId": transactionId_uuid,
  "premierStatusLevel": 0,
  "pointOfSaleCountryName": "United States",
  "catalogItems": catalogItems,
  "numberOfChildren5To11": 0,
  "serviceType": "",
  "numberOfChildren12To17": 0,
  "sessionId": sessionId_uuid,
  "isExpertModeEnabled": False,
  "getFlightsWithStops": True,
  "numberOfSeniors": 0
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