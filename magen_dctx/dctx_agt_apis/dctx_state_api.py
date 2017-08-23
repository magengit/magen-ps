# !/bin/usr/python3
from magen_utils_apis.datetime_api import datetime_parse_iso8601_string_to_utc

# Relative imports
from magen_dctx.dctx_agt_apis.dctx_item_api import DctxItem
from magen_dctx.mongo_dctx.mongo_dctx_api import MongoDctxApi

__author__ = "gibson@cisco.com"
__copyright__ = "Copyright(c) 2016, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class DctxState(DctxItem):
    """
    DctxState is the core object of dctx (device context) component,
    storing ISE-style client device information, e.g. device's posture,
    security_group, endpoint_type.
    Superclass is DctxItem: DctxState/DctxItem sit in front of mongo_dctx_*.py.

    :ivar dc_id: data context id (could be device or user)
    :ivar device_id: device (matchable with mc_id in theory)
    :ivar username: user for device
    :ivar item_data: device info (e.g. posture, security_group, endpointtype)
    :ivar creation_timestamp: time record created
    :ivar version: record versioning
    """
    # class variable: use device (rather than username) as unique key
    _dctx_state_per_device_flag = False

    def dctx_item_details(self):
        """
        Implementation of superclass abstract method.
        Returns dictionary that packages object variables

        :return: dictionary packaging object variables
        :rtype: dict
        """
        result = dict(
            dc_id=self.dc_id,
            device_id=self.device_id,
            username=self.username,
            version=self.version,
            creation_timestamp=self.creation_timestamp,
            item_data=self.item_data
        )
        return result

    _source = "DctxState"
    _projection = { "dc_id": False }

    def __init__(self):
        super().__init__(self._source)
        self.__dc_id = None
        self.__device_id = None
        self.__username = None
        self.posture = None
        self.security_group = None
        self.endpointtype = None
        self.version = None
        self.creation_timestamp = None

    @property
    def dc_id(self):
        return self.__dc_id

    @property
    def device_id(self):
        return self.__device_id

    @device_id.setter
    def device_id(self, value):
        self.__device_id = value
        if DctxState._dctx_state_per_device_flag:
            self.__dc_id = self.__device_id

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value
        if not DctxState._dctx_state_per_device_flag:
            self.__dc_id = self.__username

    def _update_dctx_state(self, dctx_state_dict):
        """
        Internal function used during processing and creation of the internal
        representation of a dctx_state.
        Update (remove and replace) the contents of the object based on
        the supplied dict

        :param dctx_state: values for update to object
        :type dctx_state_dict: dict
        """
        try:
            str_timedate = dctx_state_dict.get("creation_timestamp", None)
            self.creation_timestamp = datetime_parse_iso8601_string_to_utc(str_timedate)
            self.version = dctx_state_dict.get("version", None)

            keys = ['posture', 'security_group', 'endpointtype']
            values = [dctx_state_dict['posture'],
                      dctx_state_dict['security_group'],
                      dctx_state_dict['endpointtype']]
            self.item_data.update(dict(zip(keys, values)))
        except KeyError as e:
            self.logger.error("Failed to update client: %s.%s, error: %s", dctx_state_dict['device_id'], dctx_state_dict['username'], e)

    def create(self, dctx_state_dict):
        """
        Create the internal representation of the dctx_state
        :param dctx_state_dict: Dictionary representing a dctx_state, e.g. for update
        """

        # based on magen_events: not sure the roles of
        # create() vs. _update_dctx_state()
        self._update_dctx_state(dctx_state_dict)

        self.logger.debug("dctx_state.create: %s", dctx_state_dict)
        self.device_id = dctx_state_dict.get('device_id', None)
        self.username = dctx_state_dict.get('username', None)

    @staticmethod
    def process_update(dctx_state_dict):
        """
        Entry point for processing updates to dctx state records

        :param dctx_state_dict: Dictionary representing a client event
        :return: record written to database, stripped based on projection.
        """
        dctx_state = DctxState()
        dctx_state.create(dctx_state_dict)
        filter={'dc_id': dctx_state.dc_id}
        success, db_return = dctx_state.commit_to_db(
            filter=filter, projection=DctxState._projection)
        docs = db_return.documents if success else None
        return success, dctx_state.dc_id, docs

    @staticmethod
    def get_one_by_dc_id(dc_id=None):
        """
        Entry point for processing dctx get request

        :param dc_id: device-context key of record to return
        :return: success_indicator
        :return: database contents
        :rtype: boolean
        :rtype: dict
        """
        if DctxState._dctx_state_per_device_flag:
            return(DctxState.get_one_by_device_id(device_id=dc_id))
        else:
            return(DctxState.get_all_by_username(username=dc_id))

    @staticmethod
    def get_dctx_for_session(device_id=None, username=None):
        """
        Entry point for processing policy request for session information

        :param device_id: device for session
        :param username: username for session
        :type device_id: string
        :type username: string
        :return: success_indicator
        :return: database contents
        :rtype: boolean
        :rtype: dict
        """
        if DctxState._dctx_state_per_device_flag:
            dc_id = device_id
        else:
            dc_id = username
        return DctxState.get_one_by_dc_id(dc_id)
        
    @staticmethod
    def get_one_by_device_id(device_id=None):
        """
        Entry point for processing dctx get request
        :param device_id: device-context key of record to return
        :type device_id: string
        :return: success_indicator
        :return: state_record
        :rtype: boolean
        :rtype: dict
        """
        db_return = MongoDctxApi.get_one_by_device_id(
            device_id, projection=DctxState._projection)
        success = True if db_return.documents else False
        docs = db_return.documents if success else None
        return success, docs
    
    @staticmethod
    def get_all_by_username(username=None, projection=None):
        """
        Entry point for processing dctx get request

        :param username: filter for records to return
        :param projection: optional set of fields to be omitted from return
        :type username: dict
        :type projection: dict
        :return: success_indicator
        :return: state_records
        :rtype: boolean
        :rtype: list of dict
        """
        if projection is None:
            projection = DctxState._projection
        db_return = MongoDctxApi.get_all_by_username(
            username, projection=projection)
        success = True if db_return.documents else False
        docs = db_return.documents if success else None
        return success, docs
    
    @staticmethod
    def get_all():
        """
        Entry point for processing dctx get_all request

        :return: all state records
        :rtype: list of dict
        """
        db_return = MongoDctxApi.get_all(DctxState._projection)
        success = True if db_return.documents else False
        return success, db_return.documents
    
    @staticmethod
    def delete_one_by_dc_id(dc_id):
        """
        Entry point for processing dctx delete request

        :param device_id: dc_id key of record to delete
        :type device_id: string
        :return: deleted record
        :rtype: dict
        """
        if DctxState._dctx_state_per_device_flag:
            return(DctxState.delete_one_by_device_id(device_id=dc_id))
        else:
            return(DctxState.delete_all_by_username(username=dc_id))

    @staticmethod
    def delete_one_by_device_id(device_id):
        """
        Entry point for processing dctx delete request

        :param device_id: device key of record to delete
        :type device_id: string
        :return: deleted record
        :rtype: dict
        """
        db_return = MongoDctxApi.delete_one_by_device_id(device_id)
        success = db_return.success and db_return.count == 1
        docs = db_return.documents if success else None
        return success, docs

    @staticmethod
    def delete_all_by_username(username):
        """
        Entry point for processing dctx delete request

        :param username: username key of record to delete
        :type username: string
        :return: deleted record
        :rtype: dict
        """
        db_return = MongoDctxApi.delete_all_by_username(username)
        success = db_return.success and db_return.count >= 1
        docs = db_return.documents if success else None
        return success, docs
    
    @staticmethod
    def delete_all():
        """
        Entry point for processing dctx delete_all request

        :return: all deleted records
        :rtype: list of dicts
        """
        db_return = MongoDctxApi.delete_all()
        return db_return.success, db_return
