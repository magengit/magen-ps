"""
REST Policy Validation Messages Payload, for automated testing
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

POLICY_VALIDATION_GET_RESP_DENIED_LOCATION_MAC_LIPMAN_GET_SINGLE_SESSION_AND_SINGLE_CONTRACT = """
{
  "response": {
    "access": "denied",
    "cause_list": [
      {
        "access": "denied",
        "cause": "unauthorized location",
        "pi_uuid": "63272f8e-338a-4e04-a03a-65740e43ed14",
        "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
      }
    ],
    "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
  },
  "status": 200,
  "title": "log message"
}"""

POLICY_VALIDATION_GET_RESP_GRANTED_GENERIC = """
{
  "response": {
    "access": "granted",
    "cause": "all is well",
    "key": {
      "algorithm": "AES256",
      "asset_id": "777",
      "iv": "ut-dummy-iv",
      "key": "ut-dummy-key",
      "key_id": "ut-dummy-key-id",
      "key_server": "local",
      "state": "active",
      "ttl": 86400
    },
    "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
  },
  "status": 200,
  "title": "log message"
}
"""

POLICY_VALIDATION_GET_RESP_GRANTED_KEYLESS = """
{
  "response": {
    "access": "granted",
    "cause": "all is well",
    "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
  },
  "status": 200,
  "title": "log message"
}
"""

POLICY_VALIDATION_GET_RESP_DENIED_MISSING_MIDTOKEN = """
{
  "response": {
    "access": "denied",
    "cause": "missing required parameters: midToken",
  },
  "status": 404,
  "title": "Entitlements validation"
}"""

POLICY_VALIDATION_GET_RESP_DENIED_MISSING_ASSETID = """
{
  "response": {
    "access": "denied",
    "cause": "missing required parameters: assetId",
    "uuid": "123456789"
  },
  "status": 404,
  "title": "Entitlements validation"
}"""

POLICY_VALIDATION_GET_RESP_DENIED_MISSING_ACTION = """
{
  "response": {
    "access": "denied",
    "cause": "missing required parameters: action",
    "uuid": "123456789"
  },
  "status": 404,
  "title": "Entitlements validation"
}"""

POLICY_VALIDATION_GET_RESP_DENIED_UNKNOWN_SESSION = """
{
  "response": {
    "access": "denied",
    "cause": "client does not exist",
    "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
  },
  "status": 200,
  "title": "log message"
}"""

POLICY_VALIDATION_GET_RESP_DENIED_INVALID_ASSETID = """
{
  "response": {
    "access": "denied",
    "cause": "Asset not found",
    "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
  },
  "status": 200,
  "title": "log message"
}"""

POLICY_VALIDATION_GET_RESP_DENIED_KEY_NOTFOUND_776 = """
{
  "response": {
    "access": "denied",
    "cause": {
      "response": {
        "error": "key not found for asset ID: 776"
      },
      "status": 400,
      "title": "key details"
    },
    "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
  },
  "status": 200,
  "title": "log message"
}"""

POLICY_VALIDATION_GET_RESP_DENIED_KEY_NOTFOUND_TA = """
{
  "response": {
    "access": "denied",
    "cause": {
      "response": {
        "error": "key not found for asset ID: test_asset"
      },
      "status": 400,
      "title": "key details"
    },
    "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
  },
  "status": 200,
  "title": "log message"
}"""

POLICY_VALIDATION_GET_RESP_DENIED_DCTX_POSTURE_NO_DCTX = """
{
  "response": {
    "access": "denied",
    "cause_list": [
      {
        "access": "denied",
        "cause": "dctx state unavailable",
        "pi_uuid": "63272f8e-338a-4e04-a03a-65740e43ed14",
        "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
      }
    ],
    "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
  },
  "status": 200,
  "title": "log message"
}"""

POLICY_VALIDATION_GET_RESP_DENIED_DCTX_POSTURE_NONCOMPLIANT = """
{
  "response": {
    "access": "denied",
    "cause_list": [
      {
        "access": "denied",
        "cause": "disallowed device posture",
        "pi_uuid": "63272f8e-338a-4e04-a03a-65740e43ed14",
        "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
      }
    ],
    "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
  },
  "status": 200,
  "title": "log message"
}"""

POLICY_VALIDATION_GET_RESP_DENIED_DCTX_SECURITY_GROUP_INVALID = """
{
  "response": {
    "access": "denied",
    "cause_list": [
      {
        "access": "denied",
        "cause": "disallowed security_group type",
        "pi_uuid": "63272f8e-338a-4e04-a03a-65740e43ed14",
        "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
      }
    ],
    "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
  },
  "status": 200,
  "title": "log message"
}"""

POLICY_ENTITLEMENTS_GET_RESP_GRANTED_LOCATION = """
{
  "response": {
    "access": "granted",
    "cause": "all is well",
    "pi_uuid": "63272f8e-338a-4e04-a03a-65740e43ed14",
    "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
  },
  "status": 200,
  "title": "log message"
}
"""

POLICY_ENTITLEMENTS_GET_RESP_DENIED_LOCATION = """
{
  "response": {
    "access": "denied",
    "cause": "unauthorized location",
    "pi_uuid": "63272f8e-338a-4e04-a03a-65740e43ed14",
    "uuid": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000"
  },
  "status": 200,
  "title": "log message"
}
"""

MAGEN_ENTITLEMENTS_GET_RESP_MAC_LIPMAN_SINGLE_SESSION_SINGLE_PI = """
{
  "response": {
    "mc_id": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000",
    "expiration": "2016-07-22T20:20:16.721000+00:00",
    "r_groups": [
      {
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "environment": {
          "pdp-authorize": {
            "cookie": "7cb05384-def8-41be-b19a-11b69c2eb25c",
            "revalidation": 60
          }
        },
        "resource_group": "architecture",
        "resource_id": 1
      }
    ],
    "renewal": "2016-06-22T21:20:16.721000+00:00"
  },
  "status": 200,
  "title": "Entitlements"
}"""

MAGEN_ENTITLEMENTS_GET_RESP_MAC_LIPMAN_SINGLE_SESSION_MULTI_PI = """
{
  "response": {
    "expiration": "2016-07-22T20:25:50.640000+00:00",
    "mc_id": "06a2fdf6-4bb2-4d09-mlip-d8d92cbb0000",
    "r_groups": [
      {
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "environment": {
          "pdp-authorize": {
            "cookie": "881da7b9-499c-4c9c-856e-049dc2a7b90f",
            "revalidation": 60
          }
        },
        "resource_doc": "secret.doc",
        "resource_id": "85a41cf9-ef2e-4195-811c-d137fcf28068"
      },
      {
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "environment": {
          "pdp-authorize": {
            "cookie": "40972c39-65f2-4b5e-965e-5f254638fda1",
            "revalidation": 60
          }
        },
        "resource_group": "architecture",
        "resource_id": 1
      },
      {
          "apps": [
              "Microsoft PowerPoint",
              "Microsoft Word",
              "Microsoft Excel"
          ],
          "environment": {
              "pdp-authorize": {
                  "cookie": "97591d32-8301-4055-b658-0a9d31888f19",
                  "revalidation": 60
              }
          },
          "resource_group": "architecture",
          "resource_id": 1
      },
      {
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "environment": {
          "pdp-authorize": {
            "cookie": "924772e1-3e52-4d45-b9e6-55e6b7bd22d8",
            "revalidation": 60
          }
        },
        "resource_group": "roadmap",
        "resource_id": 3
      },
      {
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "environment": {
          "pdp-authorize": {
            "cookie": "7f2aaf6f-c4c1-4959-ab2d-2d73e511cc19",
            "revalidation": 60
          }
        },
        "resource_group": "earnings",
        "resource_id": 2
      },
      {
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "environment": {
          "pdp-authorize": {
            "cookie": "7f8ad238-68d7-42e4-8206-1c829d23f7ce",
            "revalidation": 60
          }
        },
        "resource_doc": "engineeringplans.ppt",
        "resource_id": "e2e75de2-915c-4340-abfd-5aaf743895df"
      },
      {
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "environment": {
          "pdp-authorize": {
            "cookie": "d12dcb15-6578-4afa-994f-b329652e8e38",
            "revalidation": 60
          }
        },
        "resource_group": "design",
        "resource_id": 5
      }
    ],
    "renewal": "2016-06-22T21:25:50.640000+00:00"
  },
  "status": 200,
  "title": "Entitlements"
}"""