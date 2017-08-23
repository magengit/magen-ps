MAGEN_POLICY_CONTRACT_GEOFENCE_REVERSE_GEOCODE = """
{
  "policy_contract": [
    {
      "name": "finance policy",
      "principal": "mlipman@cisco.com",
      "principal_group": "",
      "action": "open",
      "resource_group": "earnings",
      "time_validity_pi": 86400,
      "location_name": "Cisco SJC Campus>Building 10>1st Floor",
      "geofence": {
        "candidate_config": {
          "address": "",
          "lat": "37.4224764",
          "lng": "-122.0842499",
          "radius": "100"
        }
      }
    }
  ]
}
"""
MAGEN_POLICY_CONTRACT_GEOFENCE_GEOCODE = """
{
  "policy_contract": [
    {
      "name": "finance policy",
      "principal": "mlipman@cisco.com",
      "principal_group": "",
      "action": "open",
      "resource_group": "earnings",
      "time_validity_pi": 86400,
      "location_name": "Cisco SJC Campus>Building 10>1st Floor",
      "geofence": {
        "candidate_config": {
          "address": "95134",
          "lat": "",
          "lng": "",
          "radius": ""
        }
      }
    }
  ]
}
"""
MAGEN_POLICY_CONTRACT_GEOFENCE_REVERSE_GEOCODE_GET_RESP = """
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
        "creation_timestamp": "2016-11-18T07:08:51.058000+00:00",
        "geofence": {
          "applied_config": {
            "address": "Google Bldg 40, 1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA",
            "lat": 37.4223662,
            "lng": -122.0839445,
            "location_type": "ROOFTOP",
            "long_name": "Google Building 40",
            "place_id": "ChIJj38IfwK6j4ARNcyPDnEGa9g",
            "short_name": "Google Bldg 40",
            "types": [
              "premise"
            ]
          },
          "candidate_config": {
            "address": "",
            "lat": "37.4224764",
            "lng": "-122.0842499",
            "radius": "100"
          },
          "query_response": [
            {
              "address_components": [
                {
                  "long_name": "Google Building 40",
                  "short_name": "Google Bldg 40",
                  "types": [
                    "premise"
                  ]
                },
                {
                  "long_name": "1600",
                  "short_name": "1600",
                  "types": [
                    "street_number"
                  ]
                },
                {
                  "long_name": "Amphitheatre Parkway",
                  "short_name": "Amphitheatre Pkwy",
                  "types": [
                    "route"
                  ]
                },
                {
                  "long_name": "Mountain View",
                  "short_name": "Mountain View",
                  "types": [
                    "locality",
                    "political"
                  ]
                },
                {
                  "long_name": "Santa Clara County",
                  "short_name": "Santa Clara County",
                  "types": [
                    "administrative_area_level_2",
                    "political"
                  ]
                },
                {
                  "long_name": "California",
                  "short_name": "CA",
                  "types": [
                    "administrative_area_level_1",
                    "political"
                  ]
                },
                {
                  "long_name": "United States",
                  "short_name": "US",
                  "types": [
                    "country",
                    "political"
                  ]
                },
                {
                  "long_name": "94043",
                  "short_name": "94043",
                  "types": [
                    "postal_code"
                  ]
                }
              ],
              "formatted_address": "Google Bldg 40, 1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA",
              "geometry": {
                "bounds": {
                  "northeast": {
                    "lat": 37.4226621,
                    "lng": -122.0829306
                  },
                  "southwest": {
                    "lat": 37.4220703,
                    "lng": -122.0849584
                  }
                },
                "location": {
                  "lat": 37.4223662,
                  "lng": -122.0839445
                },
                "location_type": "ROOFTOP",
                "viewport": {
                  "northeast": {
                    "lat": 37.4237151802915,
                    "lng": -122.0825955197085
                  },
                  "southwest": {
                    "lat": 37.4210172197085,
                    "lng": -122.0852934802915
                  }
                }
              },
              "place_id": "ChIJj38IfwK6j4ARNcyPDnEGa9g",
              "types": [
                "premise"
              ]
            },
            {
              "address_components": [
                {
                  "long_name": "Unnamed Road",
                  "short_name": "Unnamed Road",
                  "types": [
                    "route"
                  ]
                },
                {
                  "long_name": "Mountain View",
                  "short_name": "Mountain View",
                  "types": [
                    "locality",
                    "political"
                  ]
                },
                {
                  "long_name": "Santa Clara County",
                  "short_name": "Santa Clara County",
                  "types": [
                    "administrative_area_level_2",
                    "political"
                  ]
                },
                {
                  "long_name": "California",
                  "short_name": "CA",
                  "types": [
                    "administrative_area_level_1",
                    "political"
                  ]
                },
                {
                  "long_name": "United States",
                  "short_name": "US",
                  "types": [
                    "country",
                    "political"
                  ]
                },
                {
                  "long_name": "94043",
                  "short_name": "94043",
                  "types": [
                    "postal_code"
                  ]
                }
              ],
              "formatted_address": "Unnamed Road, Mountain View, CA 94043, USA",
              "geometry": {
                "bounds": {
                  "northeast": {
                    "lat": 37.4228426,
                    "lng": -122.0833012
                  },
                  "southwest": {
                    "lat": 37.4225715,
                    "lng": -122.0849098
                  }
                },
                "location": {
                  "lat": 37.4227607,
                  "lng": -122.0840876
                },
                "location_type": "GEOMETRIC_CENTER",
                "viewport": {
                  "northeast": {
                    "lat": 37.4240560302915,
                    "lng": -122.0827565197085
                  },
                  "southwest": {
                    "lat": 37.4213580697085,
                    "lng": -122.0854544802915
                  }
                }
              },
              "place_id": "ChIJjenKhgK6j4ARVtknrvPEuFc",
              "types": [
                "route"
              ]
            },
            {
              "address_components": [
                {
                  "long_name": "Mountain View",
                  "short_name": "Mountain View",
                  "types": [
                    "locality",
                    "political"
                  ]
                },
                {
                  "long_name": "Santa Clara County",
                  "short_name": "Santa Clara County",
                  "types": [
                    "administrative_area_level_2",
                    "political"
                  ]
                },
                {
                  "long_name": "California",
                  "short_name": "CA",
                  "types": [
                    "administrative_area_level_1",
                    "political"
                  ]
                },
                {
                  "long_name": "United States",
                  "short_name": "US",
                  "types": [
                    "country",
                    "political"
                  ]
                }
              ],
              "formatted_address": "Mountain View, CA, USA",
              "geometry": {
                "bounds": {
                  "northeast": {
                    "lat": 37.469887,
                    "lng": -122.0446721
                  },
                  "southwest": {
                    "lat": 37.3567599,
                    "lng": -122.1178619
                  }
                },
                "location": {
                  "lat": 37.3860517,
                  "lng": -122.0838511
                },
                "location_type": "APPROXIMATE",
                "viewport": {
                  "northeast": {
                    "lat": 37.4508789,
                    "lng": -122.0446721
                  },
                  "southwest": {
                    "lat": 37.3567599,
                    "lng": -122.1178619
                  }
                }
              },
              "place_id": "ChIJiQHsW0m3j4ARm69rRkrUF3w",
              "types": [
                "locality",
                "political"
              ]
            },
            {
              "address_components": [
                {
                  "long_name": "94043",
                  "short_name": "94043",
                  "types": [
                    "postal_code"
                  ]
                },
                {
                  "long_name": "Mountain View",
                  "short_name": "Mountain View",
                  "types": [
                    "locality",
                    "political"
                  ]
                },
                {
                  "long_name": "Santa Clara County",
                  "short_name": "Santa Clara County",
                  "types": [
                    "administrative_area_level_2",
                    "political"
                  ]
                },
                {
                  "long_name": "California",
                  "short_name": "CA",
                  "types": [
                    "administrative_area_level_1",
                    "political"
                  ]
                },
                {
                  "long_name": "United States",
                  "short_name": "US",
                  "types": [
                    "country",
                    "political"
                  ]
                }
              ],
              "formatted_address": "Mountain View, CA 94043, USA",
              "geometry": {
                "bounds": {
                  "northeast": {
                    "lat": 37.4640869,
                    "lng": -122.0359899
                  },
                  "southwest": {
                    "lat": 37.3857439,
                    "lng": -122.10842
                  }
                },
                "location": {
                  "lat": 37.428434,
                  "lng": -122.0723816
                },
                "location_type": "APPROXIMATE",
                "viewport": {
                  "northeast": {
                    "lat": 37.4640869,
                    "lng": -122.0359899
                  },
                  "southwest": {
                    "lat": 37.3857439,
                    "lng": -122.10842
                  }
                }
              },
              "place_id": "ChIJoQmen1G3j4ARbhoe7nVBEoQ",
              "types": [
                "postal_code"
              ]
            },
            {
              "address_components": [
                {
                  "long_name": "Santa Clara County",
                  "short_name": "Santa Clara County",
                  "types": [
                    "administrative_area_level_2",
                    "political"
                  ]
                },
                {
                  "long_name": "California",
                  "short_name": "CA",
                  "types": [
                    "administrative_area_level_1",
                    "political"
                  ]
                },
                {
                  "long_name": "United States",
                  "short_name": "US",
                  "types": [
                    "country",
                    "political"
                  ]
                }
              ],
              "formatted_address": "Santa Clara County, CA, USA",
              "geometry": {
                "bounds": {
                  "northeast": {
                    "lat": 37.484637,
                    "lng": -121.208178
                  },
                  "southwest": {
                    "lat": 36.8941549,
                    "lng": -122.202476
                  }
                },
                "location": {
                  "lat": 37.3336581,
                  "lng": -121.8907041
                },
                "location_type": "APPROXIMATE",
                "viewport": {
                  "northeast": {
                    "lat": 37.484637,
                    "lng": -121.208178
                  },
                  "southwest": {
                    "lat": 36.8941549,
                    "lng": -122.202476
                  }
                }
              },
              "place_id": "ChIJd_Y0eVIvkIARuQyDN0F1LBA",
              "types": [
                "administrative_area_level_2",
                "political"
              ]
            },
            {
              "address_components": [
                {
                  "long_name": "San Jose-Sunnyvale-Santa Clara, CA",
                  "short_name": "San Jose-Sunnyvale-Santa Clara, CA",
                  "types": [
                    "political"
                  ]
                },
                {
                  "long_name": "California",
                  "short_name": "CA",
                  "types": [
                    "administrative_area_level_1",
                    "political"
                  ]
                },
                {
                  "long_name": "United States",
                  "short_name": "US",
                  "types": [
                    "country",
                    "political"
                  ]
                }
              ],
              "formatted_address": "San Jose-Sunnyvale-Santa Clara, CA, CA, USA",
              "geometry": {
                "bounds": {
                  "northeast": {
                    "lat": 37.484637,
                    "lng": -120.596562
                  },
                  "southwest": {
                    "lat": 36.1966779,
                    "lng": -122.202476
                  }
                },
                "location": {
                  "lat": 36.9374556,
                  "lng": -121.3541631
                },
                "location_type": "APPROXIMATE",
                "viewport": {
                  "northeast": {
                    "lat": 37.484637,
                    "lng": -120.596562
                  },
                  "southwest": {
                    "lat": 36.1966779,
                    "lng": -122.202476
                  }
                }
              },
              "place_id": "ChIJIXSLWpT2kYARL6cxUG2ODDQ",
              "types": [
                "political"
              ]
            },
            {
              "address_components": [
                {
                  "long_name": "San Jose Metropolitan Area",
                  "short_name": "San Jose Metropolitan Area",
                  "types": [
                    "political"
                  ]
                },
                {
                  "long_name": "California",
                  "short_name": "CA",
                  "types": [
                    "administrative_area_level_1",
                    "political"
                  ]
                },
                {
                  "long_name": "United States",
                  "short_name": "US",
                  "types": [
                    "country",
                    "political"
                  ]
                }
              ],
              "formatted_address": "San Jose Metropolitan Area, CA, USA",
              "geometry": {
                "bounds": {
                  "northeast": {
                    "lat": 37.484637,
                    "lng": -120.596562
                  },
                  "southwest": {
                    "lat": 36.1968479,
                    "lng": -122.202476
                  }
                },
                "location": {
                  "lat": 36.9374556,
                  "lng": -121.3541631
                },
                "location_type": "APPROXIMATE",
                "viewport": {
                  "northeast": {
                    "lat": 37.484637,
                    "lng": -120.596562
                  },
                  "southwest": {
                    "lat": 36.1968479,
                    "lng": -122.202476
                  }
                }
              },
              "place_id": "ChIJxwGuDoIdkoARElHtPW132v0",
              "types": [
                "political"
              ]
            },
            {
              "address_components": [
                {
                  "long_name": "California",
                  "short_name": "CA",
                  "types": [
                    "administrative_area_level_1",
                    "political"
                  ]
                },
                {
                  "long_name": "United States",
                  "short_name": "US",
                  "types": [
                    "country",
                    "political"
                  ]
                }
              ],
              "formatted_address": "California, USA",
              "geometry": {
                "bounds": {
                  "northeast": {
                    "lat": 42.0095169,
                    "lng": -114.131211
                  },
                  "southwest": {
                    "lat": 32.528832,
                    "lng": -124.482003
                  }
                },
                "location": {
                  "lat": 36.778261,
                  "lng": -119.4179324
                },
                "location_type": "APPROXIMATE",
                "viewport": {
                  "northeast": {
                    "lat": 42.009378,
                    "lng": -114.131211
                  },
                  "southwest": {
                    "lat": 32.5344766,
                    "lng": -124.415165
                  }
                }
              },
              "place_id": "ChIJPV4oX_65j4ARVW8IJ6IJUYs",
              "types": [
                "administrative_area_level_1",
                "establishment",
                "point_of_interest",
                "political"
              ]
            },
            {
              "address_components": [
                {
                  "long_name": "United States",
                  "short_name": "US",
                  "types": [
                    "country",
                    "political"
                  ]
                }
              ],
              "formatted_address": "United States",
              "geometry": {
                "bounds": {
                  "northeast": {
                    "lat": 71.5388001,
                    "lng": -66.885417
                  },
                  "southwest": {
                    "lat": 18.7763,
                    "lng": 170.5957
                  }
                },
                "location": {
                  "lat": 37.09024,
                  "lng": -95.712891
                },
                "location_type": "APPROXIMATE",
                "viewport": {
                  "northeast": {
                    "lat": 49.38,
                    "lng": -66.94
                  },
                  "southwest": {
                    "lat": 25.82,
                    "lng": -124.39
                  }
                }
              },
              "place_id": "ChIJCzYy5IS16lQRQrfeQ5K5Oxw",
              "types": [
                "country",
                "political"
              ]
            }
          ]
        },
        "location_name": "Cisco SJC Campus>Building 10>1st Floor",
        "location_zone": 9,
        "name": "finance policy",
        "principal": "mlipman@cisco.com",
        "principal_group": "",
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 86400,
        "uuid": "4228d675-a890-40f1-ae93-a6c3aed799c4"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""
MAGEN_POLICY_CONTRACT_GEOFENCE_GEOCODE_GET_RESP = """
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
        "creation_timestamp": "2016-11-18T06:53:12.113000+00:00",
        "geofence": {
          "applied_config": {
            "address": "San Jose, CA 95134, USA",
            "lat": 37.4308503,
            "lng": -121.9529992,
            "location_type": "APPROXIMATE",
            "long_name": "95134",
            "place_id": "ChIJjbOSYFTIj4ARp-EMf8nPxds",
            "short_name": "95134",
            "types": [
              "postal_code"
            ]
          },
          "candidate_config": {
            "address": "95134",
            "lat": "",
            "lng": "",
            "radius": "100"
          },
          "query_response": [
            {
              "address_components": [
                {
                  "long_name": "95134",
                  "short_name": "95134",
                  "types": [
                    "postal_code"
                  ]
                },
                {
                  "long_name": "San Jose",
                  "short_name": "San Jose",
                  "types": [
                    "locality",
                    "political"
                  ]
                },
                {
                  "long_name": "Santa Clara County",
                  "short_name": "Santa Clara County",
                  "types": [
                    "administrative_area_level_2",
                    "political"
                  ]
                },
                {
                  "long_name": "California",
                  "short_name": "CA",
                  "types": [
                    "administrative_area_level_1",
                    "political"
                  ]
                },
                {
                  "long_name": "United States",
                  "short_name": "US",
                  "types": [
                    "country",
                    "political"
                  ]
                }
              ],
              "formatted_address": "San Jose, CA 95134, USA",
              "geometry": {
                "bounds": {
                  "northeast": {
                    "lat": 37.4691679,
                    "lng": -121.915176
                  },
                  "southwest": {
                    "lat": 37.385902,
                    "lng": -121.977554
                  }
                },
                "location": {
                  "lat": 37.4308503,
                  "lng": -121.9529992
                },
                "location_type": "APPROXIMATE",
                "viewport": {
                  "northeast": {
                    "lat": 37.4691679,
                    "lng": -121.915176
                  },
                  "southwest": {
                    "lat": 37.385902,
                    "lng": -121.977554
                  }
                }
              },
              "place_id": "ChIJjbOSYFTIj4ARp-EMf8nPxds",
              "types": [
                "postal_code"
              ]
            }
          ]
        },
        "location_name": "Cisco SJC Campus>Building 10>1st Floor",
        "location_zone": 9,
        "name": "finance policy",
        "principal": "mlipman@cisco.com",
        "principal_group": "",
        "resource_group": "earnings",
        "resource_id": 2,
        "time_validity_pi": 86400,
        "uuid": "5a0f457c-ee1e-4255-afb7-042e84e6a8e7"
      }
    ],
    "success": true
  },
  "status": 200,
  "title": "Get Policy Contract"
}"""
