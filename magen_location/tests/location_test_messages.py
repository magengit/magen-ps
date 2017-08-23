# !/bin/usr/python3
"""
Examples of Location REST Messages Payload, e.g. for automated testing
Included by policy tests, since dctx/location currently included in
test environment.
"""

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__email__ = "rapenno@gmail.com"
__status__ = "alpha"

LOCATION_PUT_REQ_CAFETERIA = """
{
  "notifications": [
    {
      "notificationType": "inout",
      "subscriptionName": "Michael",
      "entity": "WIRELESS_CLIENTS",
      "deviceId": "DD.96.9F.4E.3B.11",
      "lastSeen": "2016-01-30T14:24:55.475-0800",
      "locationMapHierarchy": "Cisco SJC Campus>Building 10>1st Floor>Cafeteria",
      "locationCoordinate": {
        "x": 55.21126,
        "y": 29.913364,
        "z": 0,
        "unit": "FEET"
      },
      "geoCoordinate": {
        "latitude": -999,
        "longitude": -999,
        "unit": "DEGREES",
        "lattitude": -999
      },
      "confidenceFactor": 144,
      "apMacAddress": null,
      "ssid": null,
      "band": null,
      "floorId": 727035700041482200,
      "batteryInfo": null,
      "vendorData": null,
      "boundary": "INSIDE",
      "areaType": "FLOOR",
      "timestamp": 1454192695475
    }
  ]
}
"""

LOCATION_PUT_RESP_CAFETERIA = """
{
  "status": 200,
  "title": "mock location update",
  "response": {
    "success": true,
    "response": "Put success: status 200"
  }
}
"""

LOCATION_PUT_REQ_CFO_OFFICE = """
{
  "notifications": [
    {
      "notificationType": "inout",
      "subscriptionName": "Michael",
      "entity": "WIRELESS_CLIENTS",
      "deviceId": "DD.96.9F.4E.3B.11",
      "lastSeen": "2016-01-30T14:24:55.475-0800",
      "locationMapHierarchy": "Cisco SJC Campus>Building 10>1st Floor>CFO Office",
      "locationCoordinate": {
        "x": 55.21126,
        "y": 29.913364,
        "z": 0,
        "unit": "FEET"
      },
      "geoCoordinate": {
        "latitude": -999,
        "longitude": -999,
        "unit": "DEGREES",
        "lattitude": -999
      },
      "confidenceFactor": 144,
      "apMacAddress": null,
      "ssid": null,
      "band": null,
      "floorId": 727035700041482200,
      "batteryInfo": null,
      "vendorData": null,
      "boundary": "INSIDE",
      "areaType": "FLOOR",
      "timestamp": 1454192695475
    }
  ]
}
"""

LOCATION_PUT_RESP_CFO_OFFICE = """
{
  "response": "updated location",
  "status": 200,
  "title": "updated location"
}
"""
