# !/bin/usr/python3
"""
ReST Device Context State Message Payloads, for automated testing of dctx_agent.
Included by policy tests, since dctx/location currently included in
test environment.
"""

__author__ = "gibson@cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"

DCTX_POST_REQ_COMPLIANT_IPAD = """
{
  "magen_dctx_update": {
    "device_states": [
      {
        "device_id": "01.01.9F.4E.3B.11",
        "username": "mlipman@cisco.com",
        "posture": "compliant",
        "security_group": "engineering",
        "endpointtype": "ipad",
        "creation_timestamp": "2016-01-01T21:19:55.340000+00:00",
        "version": 1
      }
    ]
  }
}"""

DCTX_GET_RESP_COMPLIANT_IPAD = """
{
  "response": {
    "cause": "",
    "device_states": [
      {
        "device_id": "01.01.9F.4E.3B.11",
        "username": "mlipman@cisco.com",
        "item_data": {
          "posture": "compliant",
          "security_group": "engineering",
          "endpointtype": "ipad"
        },
        "creation_timestamp": "2016-01-01T21:19:55.340000+00:00",
        "version": 1
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Dctx State(s)"
}"""

DCTX_POST_REQ_NONCOMPLIANT_IPAD = """
{
  "magen_dctx_update": {
    "device_states": [
      {
        "device_id": "01.01.9F.4E.3B.11",
        "username": "mlipman@cisco.com",
        "posture": "noncompliant",
        "security_group": "engineering",
        "endpointtype": "ipad",
        "creation_timestamp": "2016-02-02T21:19:55.340000+00:00",
        "version": 1
      }
    ]
  }
}"""

DCTX_GET_RESP_NONCOMPLIANT_IPAD = """
{
  "response": {
    "cause": "",
    "device_states": [
      {
        "device_id": "01.01.9F.4E.3B.11",
        "username": "mlipman@cisco.com",
        "item_data": {
          "posture": "noncompliant",
          "security_group": "engineering",
          "endpointtype": "ipad"
        },
        "creation_timestamp": "2016-02-02T21:19:55.340000+00:00",
        "version": 1
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Dctx State(s)"
}"""

DCTX_POST_REQ_SG_DEVOPS = """
{
  "magen_dctx_update": {
    "device_states": [
      {
        "device_id": "01.01.9F.4E.3B.11",
        "username": "mlipman@cisco.com",
        "posture": "compliant",
        "security_group": "devops",
        "endpointtype": "ipad",
        "creation_timestamp": "2016-01-01T21:19:55.340000+00:00",
        "version": 1
      }
    ]
  }
}"""

DCTX_GET_RESP_SG_DEVOPS = """
{
  "response": {
    "cause": "",
    "device_states": [
      {
        "device_id": "01.01.9F.4E.3B.11",
        "username": "mlipman@cisco.com",
        "item_data": {
          "posture": "compliant",
          "security_group": "devops",
          "endpointtype": "ipad"
        },
        "creation_timestamp": "2016-01-01T21:19:55.340000+00:00",
        "version": 1
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Dctx State(s)"
}"""

DCTX_POST_REQ_COMPLIANT_MAC = """
{
  "magen_dctx_update": {
    "device_states": [
      {
        "device_id": "03.03.9F.4E.3B.11",
        "username": "amelia.brown@cisco.com",
        "posture": "compliant",
        "security_group": "finance",
        "endpointtype": "mac",
        "creation_timestamp": "2016-03-03T21:19:55.340000+00:00",
        "version": 1
      }
    ]
  }
}"""

DCTX_GET_RESP_COMPLIANT_MAC = """
{
  "response": {
    "cause": "",
    "device_states": [
      {
        "device_id": "03.03.9F.4E.3B.11",
        "username": "amelia.brown@cisco.com",
        "item_data": {
          "posture": "compliant",
          "security_group": "finance",
          "endpointtype": "mac"
        },
        "creation_timestamp": "2016-03-03T21:19:55.340000+00:00",
        "version": 1
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Dctx State(s)"
}"""

DCTX_POST_REQ_NONCOMPLIANT_MAC = """
{
  "magen_dctx_update": {
    "device_states": [
      {
        "device_id": "04.04.9F.4E.3B.11",
        "username": "paulq@cisco.com",
        "posture": "noncompliant",
        "security_group": "engineering",
        "endpointtype": "mac",
        "creation_timestamp": "2016-04-04T21:19:55.340000+00:00",
        "version": 1
      }
    ]
  }
}"""

DCTX_GET_RESP_NONCOMPLIANT_MAC = """
{
  "response": {
    "cause": "",
    "device_states": [
      {
        "device_id": "04.04.9F.4E.3B.11",
        "username": "paulq@cisco.com",
        "item_data": {
          "posture": "noncompliant",
          "security_group": "engineering",
          "endpointtype": "mac"
        },
        "creation_timestamp": "2016-04-04T21:19:55.340000+00:00",
        "version": 1
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Dctx State(s)"
}"""
