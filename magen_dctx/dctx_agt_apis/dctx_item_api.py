# !/bin/usr/python3
import logging
from abc import ABCMeta, abstractmethod

from pymongo import ReturnDocument

from magen_mongo_apis.mongo_return import MongoReturn
from magen_datastore_apis.main_db import MainDb
from magen_logger.logger_config import LogDefaults

__author__ = "gibson@cisco.com"
__copyright__ = "Copyright(c) 2016, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class DctxItem(metaclass=ABCMeta):
    """
    DctxItem is the superclass for DctxState, the only subclass.
    DctxState/DctxItem sit in front of mongo_dctx_*.py.
    """
    def __init__(self, item_source):
        self.__source = item_source
        self.__item_data = dict()
        self.logger = logging.getLogger(LogDefaults.default_log_name)

    @property
    def source(self):
        """
        :return: subclass, for debug
        """
        return self.__source

    @source.setter
    def source(self, value):
        self.__source = value

    @property
    def item_data(self):
        """
        :return: dictionary corresponding to database record
        """
        return self.__item_data

    @item_data.setter
    def item_data(self, value):
        self.__item_data = value

    def commit_to_db(self, filter=None, projection=None):
        """
        Commit item's data dictionary to database (mongoDB), returning
        results.

        :param filter: selects record to be updated
        :param projection: optional additional fields to be omitted from returned result
        :type filter: dict
        :type projection: dict
        :return: success indicator
        :return: wrapped mongo result
        :rtype: boolean
        :rtype: MongoResult
        """
        a_db = MainDb.get_instance().dctx_database
        mongo_return = MongoReturn()
        if not projection:
            projection = dict()
        projection['_id'] = False
        replace_result = a_db.dctx_items.find_one_and_replace(
            filter, self.dctx_item_details(), upsert=True,
            projection=projection,
            return_document=ReturnDocument.AFTER)
        mongo_return.success = True if replace_result else False
        if mongo_return.success:
            mongo_return.count = 1
            mongo_return.message = "Document upsert successful"
            mongo_return.documents = [replace_result]
        else:
            mongo_return.message = "Document upsert failed"
        return mongo_return.success, mongo_return

    @abstractmethod
    def dctx_item_details(self):  # subclasses must implement details routine
        pass
