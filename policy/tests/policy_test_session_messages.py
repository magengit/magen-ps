"""
ReST Policy Session Message Payloads, for automated testing.
- Naming convention:
  POLICY_SESSION_<op>_<REQ,RESP_<OK,FAIL_<why>>_<descr>[_<no,one,many>_PI]
  - <op>:                POST, PUT, GET, GET_MANY
  - <descr>:             multi-token description
  - [_<no,one,many>_PI]: get returns policy instances based on contracts
"""

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__email__ = "rapenno@gmail.com"
__status__ = "alpha"


# An array of clients to for multiple individual POSTs to session API to create
# standard clients, including multiple clients (devices) per user.
POLICY_SESSION_POST_REQS_BASELINE_CLIENTS = """
{
  "clients": [
    {
      "client": {
        "user": "alifar@cisco.com",
        "u_groups": [
             1
           ],
        "revision": "1",
        "device_id": "iphone",
        "mc_id": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
        "ip": "192.168.1.7",
        "mac": "21-70-72-8C-38-93"
      }
    },
    {
      "client": {
        "user": "paulq@cisco.com",
        "u_groups": [
             1,
             2
           ],
        "revision": "34",
        "device_id": "iphone",
        "mc_id": "05c6ae5b-a05e-45fc-9c12-f36bee79fd16",
        "ip": "192.168.1.7",
        "mac": "07-9B-4B-73-87-B0"
      }
    },
    {
      "client": {
        "user": "paulq@cisco.com",
        "u_groups": [
             1,
             2
           ],
        "revision": "35",
        "device_id": "mac",
        "mc_id": "11aae266-99ef-47c8-892c-481704b8700e",
        "ip": "192.168.1.100",
        "mac": "4C-1D-53-23-E3-F9"
      }
    },
    {
      "client": {
        "user": "repenno@cisco.com",
        "u_groups": [
             1,
             2
           ],
        "revision": "1003",
        "device_id": "mac",
        "mc_id": "d3b7b7e2-ebcd-4649-88bc-97d0eba57c27",
        "ip": "192.168.1.7",
        "mac": "7F-B2-AB-F9-A1-AE"
      }
    },
    {
      "client": {
        "user": "repenno@cisco.com",
        "u_groups": [
             1,
             2
           ],
        "revision": "10",
        "device_id": "iphone",
        "mc_id": "469c6b9c-fe85-461b-ac8a-7bde3745afcc",
        "ip": "192.168.1.20",
        "mac": "82-9C-6A-4A-B1-04"
      }
    }
  ]
}"""

# An array of expected responses to individual gets, aligned with POLICY_SESSION_POST_REQS_BASELINE_CLIENTS.
# Used e.g. to verify results of individaul posts when creating the baseline sessions.
# As sessions include policy_instances for relevant policy_contracts, get results are
# dependent on whether contracts have been created: the get results below are for the case
# where no matching contracts exist.
POLICY_SESSION_GET_RESPS_BASELINE_CLIENTS_NO_PI = """
{
  "responses": [
    {
      "response": {
        "device_id": "iphone",
        "ip": "192.168.1.7",
        "mac": "21-70-72-8C-38-93",
        "revision": "1",
        "u_groups": [
          1
        ],
        "user": "alifar@cisco.com",
        "mc_id": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
        "expiration": "2016-07-22T20:25:50.640000+00:00",
        "renewal": "2016-06-22T21:25:50.640000+00:00"
      },
      "status": 200,
      "title": "Get policy session"
    },
    {
      "response": {
        "device_id": "iphone",
        "ip": "192.168.1.7",
        "mac": "07-9B-4B-73-87-B0",
        "revision": "34",
        "u_groups": [
          1,
          2
        ],
        "user": "paulq@cisco.com",
        "mc_id": "05c6ae5b-a05e-45fc-9c12-f36bee79fd16",
        "expiration": "2016-07-22T20:25:50.640000+00:00",
        "renewal": "2016-06-22T21:25:50.640000+00:00"
      },
      "status": 200,
      "title": "Get policy session"
    },
    {
      "response": {
        "device_id": "mac",
        "ip": "192.168.1.100",
        "mac": "4C-1D-53-23-E3-F9",
        "revision": "35",
        "u_groups": [
          1,
          2
        ],
        "user": "paulq@cisco.com",
        "mc_id": "11aae266-99ef-47c8-892c-481704b8700e",
        "expiration": "2016-07-22T20:25:50.640000+00:00",
        "renewal": "2016-06-22T21:25:50.640000+00:00"
      },
      "status": 200,
      "title": "Get policy session"
    },
    {
      "response": {
        "device_id": "mac",
        "ip": "192.168.1.7",
        "mac": "7F-B2-AB-F9-A1-AE",
        "revision": "1003",
        "u_groups": [
          1,
          2
        ],
        "user": "repenno@cisco.com",
        "mc_id": "d3b7b7e2-ebcd-4649-88bc-97d0eba57c27",
        "expiration": "2016-07-22T20:25:50.640000+00:00",
        "renewal": "2016-06-22T21:25:50.640000+00:00"
      },
      "status": 200,
      "title": "Get policy session"
    },
    {
      "response": {
        "device_id": "iphone",
        "ip": "192.168.1.20",
        "mac": "82-9C-6A-4A-B1-04",
        "revision": "10",
        "u_groups": [
          1,
          2
        ],
        "user": "repenno@cisco.com",
        "mc_id": "469c6b9c-fe85-461b-ac8a-7bde3745afcc",
        "expiration": "2016-07-22T20:25:50.640000+00:00",
        "renewal": "2016-06-22T21:25:50.640000+00:00"
      },
      "status": 200,
      "title": "Get policy session"
    }
  ]
}"""

# Same info as POLICY_SESSION_GET_RESPS_BASELINE_CLIENTS, but
# when retrieved via a single get-all rather than a series of gets.
POLICY_SESSION_GETALL_RESP_BASELINE_CLIENTS_NO_PI = """
{
  "response": {
    "cause": "",
    "policy_sessions": [
      {
        "device_id" : "iphone",
        "expiration":  "2017-03-19 20:27:04.596000",
        "ip": "192.168.1.7",
        "mac" : "21-70-72-8C-38-93",
        "mc_id" : "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
        "renewal": "2017-02-17 21:27:04.596000",
        "revision": "1",
        "u_groups": [
          1
        ],
        "user": "alifar@cisco.com"
      },
      {
        "device_id": "iphone",
        "expiration": "2017-03-19 20:27:04.607000",
        "ip": "192.168.1.7",
        "mac": "07-9B-4B-73-87-B0",
        "mc_id": "05c6ae5b-a05e-45fc-9c12-f36bee79fd16",
        "renewal": "2017-02-17 21:27:04.607000",
        "revision": "34",
        "u_groups": [
          1,
          2
        ],
        "user": "paulq@cisco.com"
      },
      {
        "device_id": "iphone",
        "expiration": "2017-03-19 20:27:04.645000",
        "ip": "192.168.1.20",
        "mac": "82-9C-6A-4A-B1-04",
        "mc_id": "469c6b9c-fe85-461b-ac8a-7bde3745afcc",
        "renewal": "2017-02-17 21:27:04.645000",
        "revision": "10",
        "u_groups": [
          1,
          2
        ],
        "user": "repenno@cisco.com"
      },
      {
        "device_id": "mac",
        "expiration": "2017-03-19 20:27:04.620000",
        "ip": "192.168.1.100",
        "mac": "4C-1D-53-23-E3-F9",
        "mc_id": "11aae266-99ef-47c8-892c-481704b8700e",
        "renewal": "2017-02-17 21:27:04.620000",
        "revision": "35",
        "u_groups": [
          1,
          2
        ],
        "user": "paulq@cisco.com"
      },
      {
        "device_id": "mac",
        "expiration": "2017-03-19 20:27:04.633000",
        "ip": "192.168.1.7",
        "mac": "7F-B2-AB-F9-A1-AE",
        "mc_id": "d3b7b7e2-ebcd-4649-88bc-97d0eba57c27",
        "renewal": "2017-02-17 21:27:04.633000",
        "revision": "1003",
        "u_groups": [
          1,
          2
        ],
        "user": "repenno@cisco.com"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Sessions"
}"""

POLICY_SESSION_POST_REQ_MAC_LIPMAN = """
{
  "client": {
    "user": "mlipman@cisco.com",
    "revision": "1",
    "device_id": "mac",
    "mc_id": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000",
    "ip": "192.168.1.9",
    "mac": "DD.96.9F.4E.3B.11",
    "u_groups": [
      1,
      2
    ]
  }
}"""

POLICY_SESSION_GET_RESP_MAC_LIPMAN_NO_PI = """
{
  "response": {
    "device_id": "mac",
    "ip": "192.168.1.9",
    "mac": "DD.96.9F.4E.3B.11",
    "revision": "1",
    "u_groups": [
      1,
      2
    ],
    "user": "mlipman@cisco.com",
    "mc_id": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000",
    "expiration": "2016-07-22T20:25:50.640000+00:00",
    "renewal": "2016-06-22T21:25:50.640000+00:00"
  },
  "status": 200,
  "title": "Get policy session"
}"""

POLICY_SESSION_GET_RESP_MAC_LIPMAN_ONE_PI = """
{
  "response": {
    "device_id": "mac",
    "ip": "192.168.1.9",
    "mac": "DD.96.9F.4E.3B.11",
    "revision": "1",
    "u_groups": [
      1,
      2
    ],
    "user": "mlipman@cisco.com",
    "mc_id": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000",
    "policy_instances": ["26aaaa27-03d8-40fa-a3a4-dd578144bc31"],
    "expiration": "2016-07-22T20:25:50.640000+00:00",
    "renewal": "2016-06-22T21:25:50.640000+00:00"
  },
  "status": 200,
  "title": "Get policy session"
}"""

POLICY_SESSION_POST_REQ_LIPMAN_SCM_MAC = """
{
  "client": {
    "user": "mlipman@cisco.com",
    "revision": "1",
    "device_id": "mac",
    "mc_id": "github-mlipman-01.01.9F.4E.3B.11",
    "ip": "192.168.1.9",
    "mac": "01.01.9F.4E.3B.11",
    "u_groups": [
      1,
      2
    ]
  }
}"""

POLICY_SESSION_GET_RESP_MAC_LIPMAN_SCM_MAC_ONE_PI = """
{
  "response": {
    "device_id": "mac",
    "ip": "192.168.1.9",
    "mac": "01.01.9F.4E.3B.11",
    "revision": "1",
    "u_groups": [
      1,
      2
    ],
    "user": "mlipman@cisco.com",
    "mc_id": "github-mlipman-01.01.9F.4E.3B.11",
    "policy_instances": ["26aaaa27-03d8-40fa-a3a4-dd578144bc31"],
    "expiration": "2016-07-22T20:25:50.640000+00:00",
    "renewal": "2016-06-22T21:25:50.640000+00:00"
  },
  "status": 200,
  "title": "Get policy session"
}"""