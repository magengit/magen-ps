"""
ReST Policy Contract Message Payloads, for automated testing.

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
# POLICY CONTRACT BASIC AND LOCATION MESSAGES
#

POLICY_CONTRACT_PUT_REQ_BASELINE_CONTRACTS = """
{
  "policy_contracts": {
    "policy_contract": [
      {
        "action": "open",
        "time_validity_pi": 86400,
        "name": "Paul Quin engineering",
        "location_name": "office",
        "resource_doc": "secret.doc",
        "principal": "paulq@cisco.com",
        "principal_group": "engineering"
      },
      {
        "action": "open",
        "time_validity_pi": 432000,
        "name": "Michael Lipman Architecture",
        "location_name": "starbucks",
        "principal": "mlipman@cisco.com",
        "resource_group": "architecture",
        "principal_group": "DE"
      },
      {
        "action": "open",
        "time_validity_pi": 172800,
        "name": "Paul Quin Roadmaps",
        "location_name": "campus",
        "principal": "paulq@cisco.com",
        "resource_group": "roadmap",
        "principal_group": "DE"
      },
      {
        "action": "open",
        "time_validity_pi": 259200,
        "name": "Michael Lipman Engineering",
        "location_name": "sjc10",
        "principal": "mlipman@cisco.com",
        "resource_group": "earnings",
        "principal_group": "engineering"
      },
      {
        "action": "open",
        "time_validity_pi": 2592000,
        "name": "Marketing Plans",
        "location_name": "campus",
        "resource_doc": "marketingplans.ppt",
        "principal": "",
        "principal_group": "marketing"
      },
      {
        "action": "open",
        "time_validity_pi": 86400,
        "name": "Finance Earnings",
        "location_name": "office",
        "principal": "",
        "resource_group": "earnings",
        "principal_group": "finance"
      },
      {
        "action": "open",
        "time_validity_pi": 2592000,
        "name": "Engineering Plans",
        "location_name": "campus",
        "resource_doc": "engineeringplans.ppt",
        "principal": "",
        "principal_group": "engineering"
      },
      {
        "action": "open",
        "time_validity_pi": 86400,
        "name": "Architecture Docs",
        "location_name": "office",
        "principal": "",
        "resource_group": "architecture",
        "principal_group": "DE"
      },
      {
        "action": "open",
        "time_validity_pi": 2592000,
        "name": "Design docs",
        "location_name": "campus",
        "principal": "",
        "resource_group": "design",
        "principal_group": "engineering"
      }
    ]
  }
}"""

POLICY_CONTRACT_GETALL_RESP_BASELINE_CONTRACTS = """
{
  "response": {
    "cause": "",
    "policy_contracts": [
      {
        "PI_list": [
          "3eea52f4-eb06-4a86-8a36-479ecb231c70"
        ],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-12-07T21:50:59.843000+00:00",
        "location_name": "campus",
        "location_zone": 2,
        "name": "Paul Quin Roadmaps",
        "principal": "paulq@cisco.com",
        "principal_group": "DE",
        "principal_group_num": 2,
        "resource_group": "roadmap",
        "resource_id": 3,
        "time_validity_pi": 172800,
        "uuid": "0b090298-344f-4350-86c9-3d0ae5014dbb"
      },
      {
        "PI_list": [
          "61b479a7-d064-4d9b-b907-6c185226c95c"
        ],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-12-07T21:50:59.849000+00:00",
        "location_name": "sjc10",
        "location_zone": 3,
        "name": "Michael Lipman Engineering",
        "principal": "mlipman@cisco.com",
        "principal_group": "engineering",
        "principal_group_num": 1,
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 259200,
        "uuid": "e9760b49-9d62-4df9-95dd-75c352044266"
      },
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-12-07T21:50:59.855000+00:00",
        "location_name": "campus",
        "location_zone": 2,
        "name": "Marketing Plans",
        "principal": "",
        "principal_group": "marketing",
        "principal_group_num": 3,
        "resource_doc": "marketingplans.ppt",
        "resource_id": "cbcfd689-350f-4c2b-9044-f285b6de62d4",
        "time_validity_pi": 2592000,
        "uuid": "3434e3cc-c1a7-483e-a2dc-0df598e0af3b"
      },
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-12-07T21:50:59.856000+00:00",
        "location_name": "office",
        "location_zone": 1,
        "name": "Finance Earnings",
        "principal": "",
        "principal_group": "finance",
        "principal_group_num": 5,
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 86400,
        "uuid": "3633342b-26e2-42d8-b8c6-f38296c482c3"
      },
      {
        "PI_list": [
          "01ac6336-02b8-464c-841f-9c3139f1a035"
        ],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-12-07T21:50:59.863000+00:00",
        "location_name": "office",
        "location_zone": 1,
        "name": "Architecture Docs",
        "principal": "",
        "principal_group": "DE",
        "principal_group_num": 2,
        "resource_group": "architecture",
        "resource_id": 1,
        "time_validity_pi": 86400,
        "uuid": "0de36c31-f82e-4eb4-a1b2-dd7c35044848"
      },
      {
        "PI_list": [
          "e49baf4f-1406-42b1-91c2-9295be737e4e"
        ],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-12-07T21:50:59.869000+00:00",
        "location_name": "campus",
        "location_zone": 2,
        "name": "Design docs",
        "principal": "",
        "principal_group": "engineering",
        "principal_group_num": 1,
        "resource_group": "design",
        "resource_id": 5,
        "time_validity_pi": 2592000,
        "uuid": "f4fd5c8e-b437-47f4-8bc0-a6541e780f20"
      },
      {
        "PI_list": [
          "93a391e5-8663-4c15-aff3-64cd4c4f5b40"
        ],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-12-07T21:50:59.829000+00:00",
        "location_name": "office",
        "location_zone": 1,
        "name": "Paul Quin engineering",
        "principal": "paulq@cisco.com",
        "principal_group": "engineering",
        "principal_group_num": 1,
        "resource_doc": "secret.doc",
        "resource_id": "85a41cf9-ef2e-4195-811c-d137fcf28068",
        "time_validity_pi": 86400,
        "uuid": "16a533f9-66fe-4bb9-851c-04267e4c1ecd"
      },
      {
        "PI_list": [
          "5c862073-1742-4e91-99dd-cecb4fb339ff"
        ],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-12-07T21:50:59.837000+00:00",
        "location_name": "starbucks",
        "location_zone": 6,
        "name": "Michael Lipman Architecture",
        "principal": "mlipman@cisco.com",
        "principal_group": "DE",
        "principal_group_num": 2,
        "resource_group": "architecture",
        "resource_id": 1,
        "time_validity_pi": 432000,
        "uuid": "849ea146-ce5c-40a2-98a4-4904a33fd65b"
      },
      {
        "PI_list": [
          "5be87388-8475-4a32-b910-26e1b62ed993"
        ],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-12-07T21:50:59.857000+00:00",
        "location_name": "campus",
        "location_zone": 2,
        "name": "Engineering Plans",
        "principal": "",
        "principal_group": "engineering",
        "principal_group_num": 1,
        "resource_doc": "engineeringplans.ppt",
        "resource_id": "e2e75de2-915c-4340-abfd-5aaf743895df",
        "time_validity_pi": 2592000,
        "uuid": "a3a44681-beb5-4f80-b670-ab4a1929cca0"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contracts"
}
"""

POLICY_CONTRACT_POST_REQ_MARKETING = """
{
    "policy_contract": [
        {
            "name" : "mkt policy",
            "principal": "",
            "principal_group": "accounting",
            "action": "open",
            "resource_group": "earnings",
            "time_validity_pi" : 172800,
            "location_name": "campus"
        }
    ]
}"""

POLICY_CONTRACT_GET_RESP_MARKETING = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-05-13T05:18:42.322000+00:00",
        "location_name": "campus",
        "location_zone": 2,
        "name": "mkt policy",
        "principal": "",
        "principal_group": "accounting",
        "principal_group_num": 4,
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 172800,
        "uuid": "fb78948c-14d0-4884-b43f-8e1863a2f583"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""


# Empty location name is in request but is not included in response
POLICY_CONTRACT_POST_REQ_MARKETING_EMPTY_LOCATION_NAME = """
{
    "policy_contract": [
        {
            "name" : "mkt policy",
            "principal": "",
            "principal_group": "accounting",
            "action": "open",
            "resource_group": "earnings",
            "time_validity_pi" : 172800,
            "location_name": ""
        }
    ]
}"""


POLICY_CONTRACT_GET_RESP_MARKETING_EMPTY_LOCATION_NAME = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-06-14T13:06:54.315000+00:00",
        "name": "mkt policy",
        "principal": "",
        "principal_group": "accounting",
        "principal_group_num": 4,
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 172800,
        "uuid": "e2977a73-2d66-4961-aa92-9e5b92edec81"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""


POLICY_CONTRACT_POST_REQ_MARKETING_CUSTOM_APPS = """
{
    "policy_contract": [
        {
            "name" : "mkt policy",
            "principal": "",
            "principal_group": "accounting",
            "action": "open",
            "resource_group": "earnings",
            "time_validity_pi" : 172800,
            "location_name": "campus",
            "apps": [
                "iMovie",
                "Git",
                "AnyConnect"
            ]
        }
    ]
}"""

POLICY_CONTRACT_GET_RESP_MARKETING_CUSTOM_APPS = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "iMovie",
          "Git",
          "AnyConnect"
        ],
        "creation_timestamp": "2016-06-15T06:33:42.014000+00:00",
        "location_name": "campus",
        "location_zone": 2,
        "name": "mkt policy",
        "principal": "",
        "principal_group": "accounting",
        "principal_group_num": 4,
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 172800,
        "uuid": "75ae2315-d70b-434d-bd08-00dcf392b174"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""


POLICY_CONTRACT_POST_REQ_ENGINEERING_CAMPUS = """
{
    "policy_contract": [
        {
            "name" : "eng policy",
            "principal": "",
            "principal_group": "engineering",
            "action": "open",
            "resource_group": "architecture",
            "time_validity_pi" : 120,
            "location_name": "campus"
        }
    ]
}"""

POLICY_CONTRACT_GET_RESP_ENGINEERING_CAMPUS_NO_PI = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-05-13T05:20:27.110000+00:00",
        "location_name": "campus",
        "location_zone": 2,
        "name": "eng policy",
        "principal": "",
        "principal_group": "engineering",
        "principal_group_num": 1,
        "resource_group": "architecture",
        "resource_id": 1,
        "time_validity_pi": 120,
        "uuid": "b3288167-26ed-4eb0-8d86-b2ae8cb51f5d"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""

POLICY_CONTRACT_GET_RESP_ENGINEERING_CAMPUS_ONE_PI = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [
          "4097f457-8b59-462f-8cd9-da271ffbcb42"
        ],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-06-22T20:17:02.352000+00:00",
        "location_name": "campus",
        "location_zone": 2,
        "name": "eng policy",
        "principal": "",
        "principal_group": "engineering",
        "principal_group_num": 1,
        "resource_group": "architecture",
        "resource_id": 1,
        "time_validity_pi": 120,
        "uuid": "b9aefb20-e0e6-4c26-a201-a5d924621754"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""

POLICY_CONTRACT_GET_RESP_ENGINEERING_CAMPUS_MULTI_PI = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [
          "27d9257a-3c41-4d77-b2bf-322a856a7904",
          "99600cf2-026d-4902-bbc3-95d3d82a65c9",
          "ae546213-0727-4939-95aa-fdd7aa51c150",
          "0e6fb069-9475-4d70-b77e-958e2f0495d8",
          "842a4da2-4e34-48a9-a169-2e8fde43536f"
        ],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-07-03T05:37:25.449000+00:00",
        "location_name": "campus",
        "location_zone": 2,
        "name": "eng policy",
        "principal": "",
        "principal_group": "engineering",
        "principal_group_num": 1,
        "resource_group": "architecture",
        "resource_id": 1,
        "time_validity_pi": 120,
        "uuid": "47a5489d-1b8a-4e64-ba54-9e43154974a1"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""

# Empty location name is in request but is not included in response
POLICY_CONTRACT_POST_REQ_ENGINEERING_LOCATIONLESS = """
{
    "policy_contract": [
        {
            "name" : "eng policy",
            "principal": "",
            "principal_group": "engineering",
            "action": "open",
            "resource_group": "architecture",
            "time_validity_pi" : 120,
            "location_name": ""
        }
    ]
}"""

POLICY_CONTRACT_GET_RESP_ENGINEERING_LOCATIONLESS_NO_PI = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-05-13T05:20:27.110000+00:00",
        "name": "eng policy",
        "principal": "",
        "principal_group": "engineering",
        "principal_group_num": 1,
        "resource_group": "architecture",
        "resource_id": 1,
        "time_validity_pi": 120,
        "uuid": "b3288167-26ed-4eb0-8d86-b2ae8cb51f5d"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""

POLICY_CONTRACT_POST_REQ_FINANCE_FIRST_FLOOR = """
{
    "policy_contract": [
        {
            "name" : "finance policy",
            "principal": "mlipman@cisco.com",
            "principal_group": "",
            "action": "open",
            "resource_group": "earnings",
            "time_validity_pi" : 86400,
            "location_name": "Cisco SJC Campus>Building 10>1st Floor"
        }
    ]
}
"""

POLICY_CONTRACT_GET_RESP_FINANCE_FIRST_FLOOR_NO_PI = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-05-13T05:14:13.981000+00:00",
        "location_name": "Cisco SJC Campus>Building 10>1st Floor",
        "location_zone": 9,
        "name": "finance policy",
        "principal": "mlipman@cisco.com",
        "principal_group": "",
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 86400,
        "uuid": "2923dca3-f687-4262-aa36-38397752cfb0"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""

POLICY_CONTRACT_GET_RESP_FINANCE_FIRST_FLOOR_ONE_PI = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [
          "e9abdc59-e11d-47ae-a972-734c44632d26"
        ],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-05-13T05:16:48.028000+00:00",
        "location_name": "Cisco SJC Campus>Building 10>1st Floor",
        "location_zone": 9,
        "name": "finance policy",
        "principal": "mlipman@cisco.com",
        "principal_group": "",
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 86400,
        "uuid": "dc5d5cc3-5336-4673-bad6-abe91e1d6c8e"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""

POLICY_CONTRACT_POST_REQ_FINANCE_CFO_OFFICE_LIPMAN = """
{
    "policy_contract": [
        {
            "name" : "finance policy",
            "principal": "mlipman@cisco.com",
            "principal_group": "",
            "action": "open",
            "resource_doc": "",
            "resource_group": "earnings",
            "time_validity_pi" : 86400,
            "location_name": "Cisco SJC Campus>Building 10>1st Floor>CFO Office"
        }
    ]
}
"""

# This is used when updating/replacing the contract above
POLICY_CONTRACT_PUT_REQ_FINANCE_CFO_OFFICE_NUALA = """
{
    "policy_contract": [
        {
            "name" : "finance policy",
            "principal": "nuala@cisco.com",
            "principal_group": "",
            "action": "open",
            "resource_doc": "",
            "resource_group": "earnings",
            "time_validity_pi" : 86400,
            "location_name": "Cisco SJC Campus>Building 10>1st Floor>CFO Office"
        }
    ]
}"""

POLICY_CONTRACT_GET_RESP_FINANCE_CFO_OFFICE_LIPMAN_NO_PI = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-05-26T01:59:06.724000+00:00",
        "location_name": "Cisco SJC Campus>Building 10>1st Floor>CFO Office",
        "location_zone": 10,
        "name": "finance policy",
        "principal": "mlipman@cisco.com",
        "principal_group": "",
        "resource_doc": "",
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 86400,
        "uuid": "60c5f665-3d00-42a9-bbe7-9c355fba96bc"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""

POLICY_CONTRACT_GET_RESP_FINANCE_CFO_OFFICE_LIPMAN_ONE_PI = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [
          "a1a511ee-fcd4-4b58-b66d-5470b332f0f2"
        ],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-05-27T09:04:04.899000+00:00",
        "location_name": "Cisco SJC Campus>Building 10>1st Floor>CFO Office",
        "location_zone": 10,
        "name": "finance policy",
        "principal": "mlipman@cisco.com",
        "principal_group": "",
        "resource_doc": "",
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 86400,
        "uuid": "ac741e45-9c65-4f9b-b95b-b387c871b7f5"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""

#
# POLICY CONTRACTS REFERENCING DCTX CONSTRAINTS
#

POLICY_CONTRACT_POST_REQ_FINANCE_DCTX_POSTURE = """
{
    "policy_contract": [
        {
            "name" : "mlipman finance policy",
            "principal": "mlipman@cisco.com",
            "principal_group": "",
            "action": "open",
            "resource_group": "earnings",
            "time_validity_pi" : 86400,
            "device_posture" : "compliant"
        }
    ]
}
"""

POLICY_CONTRACT_GET_RESP_FINANCE_DCTX_POSTURE_NO_PI = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-05-13T05:18:42.322000+00:00",
        "name" : "mlipman finance policy",
        "principal": "mlipman@cisco.com",
        "principal_group": "",
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 86400,
        "device_posture" : "compliant",
        "uuid": "fb78948c-14d0-4884-b43f-8e1863a2f583"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""

POLICY_CONTRACT_POST_REQ_FINANCE_SCM_CLONE_DCTX_POSTURE = """
{
    "policy_contract": [
        {
            "name" : "mlipman finance policy",
            "principal": "mlipman@cisco.com",
            "principal_group": "",
            "action": "clone",
            "resource_group": "github",
            "time_validity_pi" : 86400,
            "device_posture" : "compliant"
        }
    ]
}
"""

POLICY_CONTRACT_GET_RESP_FINANCE_SCM_CLONE_DCTX_POSTURE_NO_PI = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [],
        "action": "clone",
        "apps": [
          "github"
        ],
        "creation_timestamp": "2016-05-13T05:18:42.322000+00:00",
        "name" : "mlipman finance policy",
        "principal": "mlipman@cisco.com",
        "principal_group": "",
        "resource_group": "github",
        "resource_id": 10,
        "time_validity_pi": 86400,
        "policy_domain" : "scm",
        "device_posture" : "compliant",
        "uuid": "fb78948c-14d0-4884-b43f-8e1863a2f583"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""

POLICY_CONTRACT_POST_REQ_FINANCE_DCTX_SG_DEVOPS = """
{
    "policy_contract": [
        {
            "name" : "mlipman finance policy",
            "principal": "mlipman@cisco.com",
            "principal_group": "",
            "action": "open",
            "resource_group": "earnings",
            "time_validity_pi" : 86400,
            "device_posture" : "compliant",
            "security_group" : "devops"
        }
    ]
}
"""

POLICY_CONTRACT_GET_RESP_FINANCE_DCTX_SG_DEVOPS_NO_PI = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-05-13T05:18:42.322000+00:00",
        "name" : "mlipman finance policy",
        "principal": "mlipman@cisco.com",
        "principal_group": "",
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 86400,
        "device_posture" : "compliant",
        "security_group" : "devops",
        "uuid": "fb78948c-14d0-4884-b43f-8e1863a2f583"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""

#
# POLICY CONTRACTS FROM TEMPLATES
#

POLICY_CONTRACT_POST_RESP_FAILED_MISSING_PT = """
{
  "response": {
    "cause": "Policy Template not found",
    "success": false,
    "uuid": null
  },
  "status": 500,
  "title": "Policy Contract Creation"
}"""

POLICY_CONTRACT_POST_REQ_MARKETING_FROM_PT_BY_NUALA = """
{
    "policy_contract": [
        {
            "name" : "nuala marketing policy",
            "principal": "amelia.brown@cisco.com",
            "principal_group": "",
            "action": "open",
            "resource_group": "roadmap",
            "time_validity_pi" : 172800,
            "location_name": "US",
            "owner": "nuala@cisco.com",
            "policy_template_name": "marketing template"
        }
    ]
}"""

POLICY_CONTRACT_GET_RESP_MARKETING_FROM_PT_BY_NUALA_NO_PI = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-05-24T03:06:29.437000+00:00",
        "location_name": "US",
        "location_zone": 5,
        "name": "nuala marketing policy",
        "owner": "nuala@cisco.com",
        "policy_template_name": "marketing template",
        "policy_template_uuid": "0b318bb3-82ed-447f-a2b7-087a134e8e24",
        "principal": "amelia.brown@cisco.com",
        "principal_group": "",
        "resource_group": "roadmap",
        "resource_id": 3,
        "time_validity_pi": 172800,
        "uuid": "444b9ad6-3911-40d6-85e8-d5c5b01970ee"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""

POLICY_CONTRACT_POST_REQ_FINANCE_FROM_PT_FIRST_FLOOR = """
{
    "policy_contract": [
        {
            "name" : "finance policy",
            "principal": "",
            "principal_group": "finance",
            "action": "open",
            "resource_group": "earnings",
            "time_validity_pi" : 86400,
            "policy_template_name": "finance template",
            "location_name": "Cisco SJC Campus>Building 10>1st Floor"
        }
    ]
}
"""

POLICY_CONTRACT_GET_RESP_FINANCE_FROM_PT_FIRST_FLOOR_NO_PI = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-05-24T02:23:10.103000+00:00",
        "location_name": "Cisco SJC Campus>Building 10>1st Floor",
        "location_zone": 9,
        "name": "finance policy",
        "policy_template_name": "finance template",
        "policy_template_uuid": "e3b1617f-d4a8-4a5e-87c9-46596a04cac4",
        "principal": "",
        "principal_group": "finance",
        "principal_group_num": 5,
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 86400,
        "uuid": "6d3ce4fe-62bf-4197-af5c-cca4505a5138"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""

POLICY_CONTRACT_POST_REQ_FINANCE_FROM_PT_BY_NUALA_FOR_ROD = """
{
    "policy_contract": [
        {
            "name" : "nuala finance policy",
            "principal": "rod.thompson@cisco.com",
            "principal_group": "",
            "action": "open",
            "resource_group": "earnings",
            "time_validity_pi" : 172800,
            "location_name": "campus",
            "owner": "nuala@cisco.com",
            "policy_template_name": "finance template"
        }
    ]
}"""

POLICY_CONTRACT_GET_RESP_FINANCE_FROM_PT_BY_NUALA_FOR_ROD_NO_PI = """
{
  "response": {
    "cause": null,
    "policy_contract": [
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-05-24T03:04:33.191000+00:00",
        "location_name": "campus",
        "location_zone": 2,
        "name": "nuala finance policy",
        "owner": "nuala@cisco.com",
        "policy_template_name": "finance template",
        "policy_template_uuid": "12ce6832-3e36-4c5d-b040-05cda9a9cb90",
        "principal": "rod.thompson@cisco.com",
        "principal_group": "",
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 172800,
        "uuid": "6c8269b1-92c7-4254-bb0c-be99f5ebab7a"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""

POLICY_CONTRACT_GET_MANY_RESP_FROM_PT_BY_NUALA = """
{
  "response": {
    "cause": "",
    "policy_contracts": [
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-05-24T03:07:11.292000+00:00",
        "location_name": "campus",
        "location_zone": 2,
        "name": "nuala finance policy",
        "owner": "nuala@cisco.com",
        "policy_template_name": "finance template",
        "policy_template_uuid": "7ce70b27-0fa2-4dc9-8880-a4e2af7445fc",
        "principal": "rod.thompson@cisco.com",
        "principal_group": "",
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 172800,
        "uuid": "42ac473d-4453-4926-8c9a-b0f826491497"
      },
      {
        "PI_list": [],
        "action": "open",
        "apps": [
          "Microsoft PowerPoint",
          "Microsoft Word",
          "Microsoft Excel"
        ],
        "creation_timestamp": "2016-05-24T03:07:14.544000+00:00",
        "location_name": "US",
        "location_zone": 5,
        "name": "nuala marketing policy",
        "owner": "nuala@cisco.com",
        "policy_template_name": "marketing template",
        "policy_template_uuid": "dd63c5cd-f04e-4305-a505-9ea7f9c3db60",
        "principal": "amelia.brown@cisco.com",
        "principal_group": "",
        "resource_group": "roadmap",
        "resource_id": 3,
        "time_validity_pi": 172800,
        "uuid": "851a1e87-879a-4232-a585-e3364a00bcb0"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contracts"
}"""
