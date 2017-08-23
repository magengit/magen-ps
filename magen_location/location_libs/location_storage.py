#! /usr/bin/python3
"""
Storage has a collection of location_validators
the access and search inside the collection has to be effective
Implementing hash-table based on python dictionary
Consuming point for a web-socket service to implement event driven architecture
Web-sockets are chosen for demo purposes. Going to be shipped to Message Bus in future
"""
import logging
import threading

# Package imports from local PIP
from magen_logger.logger_config import LogDefaults

__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class LocationStore(object):
    _instance = None

    def __init__(self):
        if self._instance is not None:
            raise ValueError("An instantiation of the singleton class already exists!")
        self._validators = dict()
        self._trackers = dict()
        self._threadLock = threading.Lock()
        self.logger = logging.getLogger(LogDefaults.default_log_name)

    # FIXME: store trackers by key
    # FIXME: change validators to use opaque/unique key instead of mac_address (so you can use other addresses - Mac, IP, MAC+IP)
    # FIXME: add locks if MT support needed
    # add, remove, get tracker for remote tracking
    # called from LCTX when added or removed to track external dependencies
    # returns the storage dictionary - should not be used for normal purposes
    @property
    def trackers(self):
        return self._trackers

    @trackers.setter
    def trackers(self, value):
        assert False, "trackers does not support assignment"
        pass

    def remove_all_trackers(self):
        self._trackers.clear()

    def add_tracker(self, key, new_tracker):
        tracker = self._trackers.get(key, None)
        if tracker is None:
            self._trackers[key] = new_tracker
            return True
        else:
            self.logger.error("add_tracker: already exists for key: %s", key)
            return False

    def remove_tracker(self, key):
        tracker = self._trackers.get(key, None)
        if tracker is None:
            self.logger.error("remove_tracker: does not exist for key: %s", key)
            return False
        else:
            self._trackers.pop(key)
            return True
        
    def get_tracker(self, key):
        tracker = self._trackers.get(key, None)
        return tracker

    # returns the storage dictionary - should not be used for normal purposes
    @property
    def validators(self):
        return self._validators

    @validators.setter
    def validators(self, value):
        self.logger.debug('no support for setting location validators')
        pass

    def add_validator(self, new_validator):
        # print("add_validator:", new_validator.mac_address, new_validator)
        mac_address = new_validator.mac_address
        validator_list = self._validators.get(mac_address)
        mc_id = new_validator.client_mc_id
        pi_uuid = new_validator.policy_instance
        # check for replacing validator
        if validator_list:
            len_before = len(validator_list)
            # Lock the update of validator store
            self._threadLock.acquire(True)
            self._validators[mac_address] = [v for v in validator_list if not (v.client_mc_id == mc_id and v.policy_instance == pi_uuid)]
            self._validators[mac_address].append(new_validator)
            len_after = len(self._validators[mac_address])
            self._threadLock.release()
            if len_before == len_after:
                self.logger.debug("add_validator: replaced with new validator %s len=%d", new_validator, len_after)
            else:
                self.logger.debug("add_validator: added new validator %s len= %d", new_validator, len_after)
        else:
            # add new validator
            # Lock the update of validator store
            self._threadLock.acquire(True)
            self._validators[mac_address] = []
            self._validators[mac_address].append(new_validator)
            self._threadLock.release()
            self.logger.debug("add_validator: inserted new validator %s", new_validator)
        return new_validator

    def remove_validator(self, existing_validator):
        self.logger.debug("remove_validator: %s, %s", existing_validator.mac_address, existing_validator)
        pi = existing_validator.policy_instance
        validator_list = self._validators.get(existing_validator.mac_address)
        if validator_list:
            # FIXME: removes all validators for client -> PI is the unique key for validator
            new_list = [v for v in validator_list if not v.policy_instance == pi]
            # Lock the update of validator store
            self._threadLock.acquire(True)
            if new_list:
                self._validators[existing_validator.mac_address] = new_list
            else:
                self._validators.pop(existing_validator.mac_address)
            self._threadLock.release()

    def remove_all_validators(self):
        self._validators.clear()

    def get_validator_list(self, mac_address, mc_id=None, pi_uuid=None):
        # no need to lock the get of the validator list
        validator_list = self._validators.get(mac_address)
        if validator_list:
            if mc_id and pi_uuid:  # return only the specific PI for the client
                return [v for v in validator_list if (v.client_mc_id == mc_id and v.policy_instance == pi_uuid)]
            elif mc_id:  # return all PIs for the client
                return [v for v in validator_list if (v.client_mc_id == mc_id)]
            elif pi_uuid:  # return only the PI matching mac_address (client ignored)
                return [v for v in validator_list if (v.policy_instance == pi_uuid)]
            else:  # return all clients and PIs for the given MAC
                return validator_list
        else:
            return list()
    
    def validator_exists(self, mac_address):
        validator_list = self._validators.get(mac_address)
        if validator_list:
            return True
        else:
            return False
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
