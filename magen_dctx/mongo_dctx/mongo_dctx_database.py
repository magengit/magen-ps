# !/bin/usr/python3
import logging

from magen_datastore_apis.dao_interface import IDao
from magen_datastore_apis.main_db import MainDb
from pymongo import MongoClient

from magen_logger.logger_config import LogDefaults
from magen_datastore_apis.utils_db import IUtils

__author__ = "gibson@cisco.com"
__copyright__ = "Copyright(c) 2016, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"

MONGO_PORT = 27017
MONGO_IP = '127.0.0.1'
LOCAL_MONGO_LOCATOR = "{ip}:{port}".format(ip=MONGO_IP, port=MONGO_PORT)


class MongoDctxDb(MainDb):
    """
    Mongo database/collection setup for DctxItem.
    (Compare MongoDctxDb, MongoDctxApi)

    Attributes:
        _instance             instance for this singleton class
        mongo_client          client handle to talk to mongodb server
        dctx_db               mongodb database on server
        dctx_items            mongodb collection within database

    :ivar dctx_db: superclass database collection
    :ivar db_ip_port: ip port for database (e.g. mongodb)
    :ivar dctx_item_strategy:
    :ivar utils_strategy:
    """

    _instance = None
    mongo_client = None

    dctx_db = None
    dctx_items = None

    def __init__(self):
        super().__init__()
        self.__db_ip_port = LOCAL_MONGO_LOCATOR
        self.__dctx_item_strategy = IDao
        self.__utils_strategy = IUtils

    @property
    def dctx_item_strategy(self):
        return self.__dctx_item_strategy

    @dctx_item_strategy.setter
    def dctx_item_strategy(self, value):
        self.__dctx_item_strategy = value

    @property
    def db_ip_port(self):
        """DB Element Strategy"""
        return self.__db_ip_port

    @db_ip_port.setter
    def db_ip_port(self, value):
        self.__db_ip_port = value

    def get_dctx_db(self):
        return self.dctx_db

    def get_dctx_items(self):
        return self.dctx_items

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize(self):
        """
        Initialize dctx mongo collection
        """
        logger = logging.getLogger(LogDefaults.default_log_name)
        logger.info("dctx database initalize...")
        self.mongo_client = MongoClient(self.db_ip_port)
        # items collections
        self.dctx_db = self.mongo_client.get_database('dctx_db')
        self.dctx_items = self.dctx_db.get_collection('dctx_items')
