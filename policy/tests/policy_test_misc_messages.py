"""
ReST Misc Payloads, for automated testing.

- Naming convention:
  POLICY_CONTRACT_<op>_<REQ,RESP_<OK,FAIL_<why>>_<descr>[_<no,one,many>_PI]
  - <op>:                POST, PUT, GET, GET_MANY
  - <descr>:             multi-token description
  - [_<no,one,many>_PI]: get returns policy instances based on sessions
"""

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__email__ = "rapenno@gmail.com"
__status__ = "alpha"

#
# POLICY MISC MESSAGES
#

POLICY_MISC_GET_RESP_CHECK = """
{
  "response": {
    "level": "40",
    "success": true
  },
  "status": 200,
  "title": "Get Level"
}
"""

POLICY_MISC_POST_LOGGING_LEVEL_INFO = """
{
  "level": "info" 
}
"""

POLICY_MISC_GET_RESP_LOGGING_LEVEL_ERROR = """
{
  "response": {
    "level": 40,
    "success": true
  },
  "status": 200,
  "title": "logging_level"
}
"""

POLICY_MISC_GET_RESP_LOGGING_LEVEL_INFO = """
{
  "response": {
    "level": 20,
    "success": true
  },
  "status": 200,
  "title": "logging_level"
}
"""

POLICY_MISC_GET_RESP_LOGGING_LEVEL_DEBUG = """
{
  "response": {
    "level": 10,
    "success": true
  },
  "status": 200,
  "title": "logging_level"
}
"""
