"""
ReST Policy Template Message Payloads, for automated testing.

policy_template unit test messages

- Naming convention:
  POLICY_TEMPLATE_<op>_<REQ,RESP_<OK,FAIL_<why>>_<descr>
  - <op>:                POST, PUT, GET, GET_MANY
  - <descr>:             multi-token description
"""

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__email__ = "rapenno@gmail.com"
__status__ = "alpha"

POLICY_TEMPLATE_POST_RESP_OK = """
{
  "response": {
    "cause": null,
    "success": true,
    "uuid": "ba84deea-c2a9-4d47-9337-95b424a67fdc"
  },
  "status": 200,
  "title": "Create Policy Template"
}"""

POLICY_TEMPLATE_POST_REQ_FINANCE = """
{
    "policy_template": [
        {
            "name" : "finance template",
            "principal": "",
            "principal_group": "finance",
            "action": "create",
            "policy_contracts": [],
            "uuid": ""
        }
    ]
}"""

POLICY_TEMPLATE_POST_REQ_ACCOUNTING = """
{
    "policy_template": [
        {
            "name" : "accounting template",
            "principal": "",
            "principal_group": "accounting",
            "action": "create",
            "policy_contracts": [],
            "uuid": ""
        }
    ]
}"""


POLICY_TEMPLATE_POST_REQ_MARKETING = """
{
    "policy_template": [
        {
            "name" : "marketing template",
            "principal": "",
            "principal_group": "marketing",
            "action": "create",
            "policy_contracts": [],
            "uuid": ""
        }
    ]
}"""


POLICY_TEMPLATE_GET_RESP_MARKETING = """
{
  "response": {
    "cause": null,
    "policy_template": [
      {
        "action": "create",
        "action_id": 1,
        "name": "marketing template",
        "policy_contracts": [],
        "principal": "",
        "principal_group": "marketing",
        "uuid": "a73366aa-94bc-4e0b-abcf-024bf35e7310"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Template"
}"""

POLICY_TEMPLATE_GET_RESP_FINANCE = """
{
  "response": {
    "cause": null,
    "policy_template": [
      {
        "action": "create",
        "action_id": 1,
        "name": "finance template",
        "policy_contracts": [],
        "principal": "",
        "principal_group": "finance",
        "uuid": "6e014c53-cf4a-4ed7-a7ff-dabb3fbb626e"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Template"
}"""

POLICY_TEMPLATE_GET_RESP_ACCOUNTING = """
{
  "response": {
    "cause": null,
    "policy_template": [
      {
        "action": "create",
        "action_id": 1,
        "name": "accounting template",
        "policy_contracts": [],
        "principal": "",
        "principal_group": "accounting",
        "uuid": "2cdb1645-c9ee-4fa9-b0d9-24f7af867fa2"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Template"
}"""

POLICY_TEMPLATE_GET_MANY_RESP_USER_FILTER = """
{
  "response": {
    "cause": "",
    "policy_templates": [
      {
        "action": "create",
        "action_id": 1,
        "name": "finance template",
        "policy_contracts": [],
        "principal": "",
        "principal_group": "finance",
        "uuid": "9a436816-5106-4b7d-99ef-f2232544d63e"
      },
      {
        "action": "create",
        "action_id": 1,
        "name": "accounting template",
        "policy_contracts": [],
        "principal": "",
        "principal_group": "accounting",
        "uuid": "51d75196-1538-4492-84e7-bc28fb28cc30"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Templates"
}"""


