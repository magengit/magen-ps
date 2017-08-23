"""
Interface to shared mongo-db collection
"""

# Package imports from local PIP
from magen_datastore_apis.main_db import MainDb

# Relative imports
from magen_dctx.mongo_dctx.mongo_dctx_database import MongoDctxDb
from magen_dctx.mongo_dctx.mongo_dctx_api import MongoDctxApi

__author__ = "gibson@cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


def dctx_agt_db_init(mongo_ip_port):
    db = MainDb.get_instance()
    db.dctx_database = MongoDctxDb.get_instance()
    db.dctx_database.dctx_item_strategy = MongoDctxApi.get_instance()
    db.dctx_database.db_ip_port = mongo_ip_port
    db.dctx_database.initialize()

