"""
REST Service Messages Payload, for automated testing

Response messages to use when mocking other services that policy
talks to operationally. (In other words, the policy_test_<xxx>_messages
are the test load, whereas these are the emulated responses when the
policy test messages trigger policy to consult other services.

- Naming convention:
  POLICY_VALIDATION_<op>_<REQ,RESP_<GRANTED,DENIED_<why>>
  - <op>:                POST, PUT, GET, GET_MANY
  - <descr>:             multi-token description
  - [_<no,one,many>_PI]: get returns policy instances based on contracts
"""

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__email__ = "rapenno@gmail.com"
__status__ = "alpha"

###########################################################################
#
# INGESTION SERVICE: response message mocks
#
###########################################################################

INGESTION_ASSET_GET_RESP_FOUND = """
{
  "response": {
    "asset": [
      {
        "client_uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000",
        "creation_timestamp": "2016-09-01T21:22:13.053000+00:00",
        "host": "sjc-repenno-nitro10.cisco.com",
        "name": "finance doc",
        "resource_group": "earnings",
        "resource_id": 2,
        "uuid": "1c43ae97-ce17-43cc-a90e-8733928ebb69",
        "version": 1
      }
    ],
    "cause": "Asset found",
    "success": true
  },
  "status": 200,
  "title": "Get Asset"
}"""

INGESTION_ASSET_GET_RESP_NOTFOUND = """
{
  "response": {
    "asset": [],
    "cause": "Asset not found",
    "success": true
  },
  "status": 404,
  "title": "Get Asset"
}"""

###########################################################################
#
# KEY SERVICE: response message mocks
#
###########################################################################

KEYSVC_ASSET_GET_RESP_NOTFOUND = """
{
  "response": {
    "error": "key not found for asset ID: test_asset"
  },
  "status": 400,
  "title": "key details"
}
"""
