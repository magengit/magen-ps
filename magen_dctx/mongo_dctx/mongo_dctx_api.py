# !/bin/usr/python3
# Package imports from local PIP
from magen_datastore_apis.main_db import MainDb
from magen_mongo_apis.concrete_dao import Dao

__author__ = "gibson@cisco.com"
__copyright__ = "Copyright(c) 2016, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class MongoDctxApi(Dao):
    """
    Mongo database/collection API routines
    (Compare MongoDctxDb, MongoDctxApi)
    """

    @staticmethod
    def __get_db():
        """
        return dctx_db: mongo database for dctx items collection
        """
        # Could add to main_db.py (matching other dbs): full ref seems clearer
        # db = MainDb.get_dctx_db_instance()
        db = MainDb.get_instance().dctx_database
        return db

    def get_collection(self):
        """
        return dctx_items: collection within dctx_db mongo database
        """
        db = MongoDctxApi.__get_db()
        return db.get_dctx_items()

    @staticmethod
    def get_one_by_device_id(device_id, projection=None):
        """
        Return DB dctx_item record corresponding to supplied device_id

        :param device_id: device for which mongodb record is wanted
        :param projection: optional restriction on which record fields should be returned
        :type device_id: string
        :type projection: dict
        :return: db record, wrapped by db lookup status
        :rtype: MongoReturn
        """
        db = MongoDctxApi.__get_db()
        db_return = db.dctx_item_strategy.select_by_condition({"device_id": device_id}, projection=projection)
        return db_return

    @staticmethod
    def get_all_by_username(username, projection=None):
        """
        Return all DB dctx_item records for supplied username.
        (Currently expected to be at most one, until multidevice is needed.)

        :param username: user for which mongodb record(s) are wanted
        :param projection: optional restriction on which record fields should be returned
        :type device_id: string
        :type projection: dict
        :return: db record(s), wrapped by db lookup status
        :rtype: MongoReturn
        """
        db = MongoDctxApi.__get_db()
        db_return = db.dctx_item_strategy.select_by_condition({"username": username}, projection=projection)
        return db_return

    @staticmethod
    def get_all(projection=None):
        """
        Return all DB dctx_item records

        :param username: user for which mongodb record(s) are wanted
        :param projection: optional restriction on which record fields should be returned
        :type device_id: string
        :type projection: dict
        :return: db records, wrapped by db lookup status
        :rtype: MongoReturn
        """
        db = MongoDctxApi.__get_db()
        db_return = db.dctx_item_strategy.select_all(projection=projection)
        return db_return

    @staticmethod
    def delete_one_by_device_id(device_id):
        """
        Delete one dctx item record from DB.

        :param username: username
        :return: contents of deleted record
        :rtype: MongoReturn
        """
        db = MongoDctxApi.__get_db()
        if not device_id:
            raise ValueError
        seed = {"device_id": device_id}
        db_return = db.dctx_item_strategy.delete(seed)
        return db_return

    @staticmethod
    def delete_all_by_username(username):
        """
        Delete dctx item records for user from DB.

        :param username: username
        :return: contents of deleted records
        :rtype: MongoReturn
        """
        db = MongoDctxApi.__get_db()
        if not username:
            raise ValueError
        seed = {"username": username}
        db_return = db.dctx_item_strategy.delete(seed)
        return db_return

    @staticmethod
    def delete_all():
        """
        Delete all dctx item records from DB.

        :return: contents of deleted records
        :rtype: MongoReturn
        """
        db = MongoDctxApi.__get_db()
        db_return = super(MongoDctxApi, db.dctx_item_strategy).delete_all()
        return db_return
