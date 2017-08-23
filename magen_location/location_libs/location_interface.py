#! /usr/bin/python3
import json
import logging
import re
import sys

from math import radians, cos, sin, asin, sqrt

from magen_logger.logger_config import LogDefaults

from magen_location.location_apis.location_validator import LocationValidator, LctxLocation
from magen_location.location_libs.location_storage import LocationStore

location_store = LocationStore.get_instance()


class LocationApi(object):

    @staticmethod
    def start_location_tracking(pi_uuid, client_info, location_constraint):
        if isinstance(
                client_info,
                dict) and isinstance(
                location_constraint,
                dict):
            return _start_location_tracking(
                pi_uuid, client_info, location_constraint)
        else:
            raise TypeError("dictionaries expected")

    @staticmethod
    def stop_location_tracking(mac_address, mc_id=None, pi_uuid=None):
        return _stop_location_tracking(
            mac_address, mc_id=mc_id, pi_uuid=pi_uuid)

    @staticmethod
    def mock_location_update(lctx_location_update):
        return _mock_location_update(lctx_location_update)

    @staticmethod
    def location_update(lctx_location_update):
        return _location_update(lctx_location_update)

    @staticmethod
    def show_location_validators():
        return _show_location_validators()

    @staticmethod
    def show_location_trackers():
        return _show_location_trackers()

    @staticmethod
    def clear_location_validators():
        location_store.remove_all_validators()
        return

    @staticmethod
    def clear_location_trackers():
        location_store.remove_all_trackers()
        return

    @staticmethod
    def location_tracking_enabled(mac_address):
        return location_store.validator_exists(mac_address)

    @staticmethod
    def get_current_location_constraint(pi_uuid, mac_address):
        """
        Retrieve location string from location validator store
        :param pi_uuid, mac_address: pi_uuid and mac_address for selecting constraint
        :return: location name
        """
        logger = logging.getLogger(LogDefaults.default_log_name)
        location_name = None

        l_val_list = location_store.get_validator_list(mac_address, pi_uuid=pi_uuid)
        if not l_val_list:
            # TODO: populate validators on restart
            logger.info(
                "get_current_location_constraint validator not found - did you restart server ?")
            result = {}
            return result
        else:
            # should only find one validator matching PI
            assert len(l_val_list) == 1
            for validator in l_val_list:
                location_constraint = validator.location_constraint
                if location_constraint != {}:
                    return location_constraint
            logger.debug("location constraint not found for mac=%s pi=%s", mac_address, pi_uuid)
            return {}
            

# TODO: support multiple clients per MAC, support location by IP address and/or MAC
# support multiple PIs per client (need to match by PI_uuid on insert and remove and process event)
# FIXME: convert location_constraint to a location object (same as
# LctxLocation) and pass all the way through


def _start_location_tracking(pi_uuid, client_info, location_constraint):
    logger = logging.getLogger(LogDefaults.default_log_name)

    mac = client_info.get("mac_address", "")
    mc_id = client_info.get("mc_id", "")
    location_name = location_constraint.get("location_name", "")
    zone_id = location_constraint.get("location_zone", 0)
    geocoordinate = {} # this is for geolocation - supported
    coordinate = {} # this is for x,y map coordinates - Not supported yet

    # NOTE: temporary support of geolocation
    # location_name will be string with embedded dictionary for geolocation coordinates
    # {'Geolocation': {'longitude': 10.0, 'radius_unit': 'FEET', 'radius': 10, 'latitude': 10.0, 'unit': 'DEGREES'}}
    if re.match("{\"Geolocation\":", location_name):
        geocoordinate = json.loads(location_name).get('Geolocation')
        logger.debug("geocoordinate: %s", geocoordinate)

    # make sure we have a mac address, mc_id and location name
    if mac and mc_id and location_name:
        location_validator = LocationValidator(mac_address=mac,
                                               mc_id=mc_id,
                                               policy_instance_uuid=pi_uuid,
                                               location=location_name,
                                               coordinate=coordinate,
                                               geocoordinate=geocoordinate,
                                               zone_id=zone_id)

        location_store.add_validator(location_validator)
        # print("LS:", location_store.validators)
        return location_validator.get_details()
    else:
        logger.error(
            "invalid arguments: PI=%s client=%s location=%s",
            pi_uuid,
            client_info,
            location_constraint)
        return {}


def _stop_location_tracking(mac_address, mc_id=None, pi_uuid=None):
    logger = logging.getLogger(LogDefaults.default_log_name)

    validator_list = location_store.get_validator_list(
        mac_address, mc_id=mc_id, pi_uuid=pi_uuid)
    if validator_list:
        for validator in validator_list:
            location_store.remove_validator(validator)
        return True
    else:
        logger.info(
            "_stop_location_tracking: validator_list not found MAC: %s, Client: %s, PI: %s\n",
            mac_address,
            mc_id,
            pi_uuid)
        return False

# FIXME: use this for internal unit tests and demo scenarios without LCTX


def _mock_location_update(lctx_location_update):
    assert isinstance(lctx_location_update,
                      dict), "lctx_location_update must be a dictionary"
    return _process_location_update(lctx_location_update)


def _location_update(lctx_location_update):
    assert isinstance(lctx_location_update,
                      dict), "lctx_location_update must be a dictionary"
    return _process_location_update(lctx_location_update)


def _process_location_update(lctx_location_update):
    """
    Update the location validator based on current location
    :param lctx_location_update structure
    :return: list of [{"pi_uuid": pi_uuid, "valid": valid}, ...] for PIs that changed
    """
    logger = logging.getLogger(LogDefaults.default_log_name)

    logger.debug("process_location_update: %s", lctx_location_update)
    notification_type = lctx_location_update["notificationType"]

    client_mac_address = lctx_location_update["deviceId"]
    client_map_hierarchy = lctx_location_update["locationMapHierarchy"]
    client_location_coordinate = lctx_location_update["locationCoordinate"]
    client_location_geocoordinate = lctx_location_update["geoCoordinate"]

    # Note: assuming caller has filled in the boundary properly
    client_boundary = lctx_location_update["boundary"]

    # FIXME: zone unknown at this point - set to 0
    lctx_location = LctxLocation(map_hierarchy=client_map_hierarchy,
                               coordinate=client_location_coordinate,
                               geocoordinate=client_location_geocoordinate,
                               boundary=client_boundary,
                               zone_id=0)

    validator_list = location_store.get_validator_list(client_mac_address)
    # debug
    logger.debug("MAC: %s LCTX: %s", client_mac_address, lctx_location)
    logger.debug("Validator_list: %s\n", validator_list)

    updated_validators = list()
    for validator in validator_list:
        # Note: we separate the location_store and service from the PDP server
        # we will do the local check of current location vs. location constraint here and return the update
        # It's up to the caller to decide to update the PDP

        previous_location_valid = validator.location_valid
        logger.debug(
            "check validator: was valid? = %s",
            previous_location_valid)
        logger.debug(
            "  curloc: %s \n  constraint: %s\n",
            lctx_location,
            validator.location_constraint)

        # create a lctx location equality comparison function
        # check location update against the location constraint stored in the
        # validator
        location_valid = False
        location_distance = -1

        # do a regular expression match for zones (current location within constraint)
        # FIXME: deal with boundaries properly
        # NOTE: first check if this is a geolocation constraint
        if validator.location_constraint.geocoordinate != {}:
            logger.debug("geolocation constraint check: constraint=%s current=%s",
                         validator.location_constraint.geocoordinate, lctx_location.geocoordinate)
            geocoordinate = validator.location_constraint.geocoordinate
            latitude = geocoordinate.get('latitude', None)
            longitude = geocoordinate.get('longitude', None)
            radius = geocoordinate.get('radius', None)
            unit = geocoordinate.get('unit', None)
            radius_unit = geocoordinate.get('radius_unit', None)

            # make sure correct types passed in
            assert (type(latitude) == float and type(longitude) == float and (type(radius) == float or type(radius) == int)), "geolocation constraint incorrect types"
            # check if constraint is valid
            if latitude and longitude and radius and unit == "DEGREES" and radius_unit == "METERS":
                # now get the current geocoordinate from the lctx_update
                lctx_geocoordinate = lctx_location.geocoordinate
                lctx_latitude = lctx_geocoordinate.get('latitude', -999.0)
                lctx_longitude = lctx_geocoordinate.get('longitude', -999.0)
                lctx_unit = lctx_geocoordinate.get('unit', None)

                # make sure correct types passed in
                assert (type(lctx_latitude) == float and type(lctx_longitude) == float), "lctx_location constraint incorrect types"
                if lctx_unit == "DEGREES" and lctx_latitude >= -90.0 and lctx_latitude <= 90.0 and lctx_longitude >= -180.0 and lctx_longitude <= 180.0:
                    location_distance = haversine(longitude, latitude, lctx_longitude, lctx_latitude)
                    logger.info("distance: %s constraint=%s current=%s", location_distance, geocoordinate, lctx_geocoordinate)
                    
                    # Note: may need to add a fudge factor, add support for polygons, 
                    # support for OUTSIDE boundary constraint, etc.
                    # The boundary for geolocation only matters for the constraint
                    # If "INSIDE" then check distance <= radius otherwise check distance > radius
                    if location_distance <= radius:
                        if validator.location_constraint.boundary == "INSIDE":
                            location_valid = True
                            logger.debug("location valid: inside boundary")
                        else: 
                            location_valid = False
                            logger.debug("location not valid: outside boundary")
                    else:
                        if validator.location_constraint.boundary == "OUTSIDE":
                            location_valid = True
                            logger.debug("location valid: outside boundary")
                        else:
                            location_valid = False
                            logger.debug("location not valid: outside boundary")
                else:
                    location_valid = False
                    logger.info("invalid or out of range lctx geolocation lat=%s lon=%s unit=%s", lctx_latitude, lctx_longitude, lctx_unit)
            else:
                location_valid = False
                logger.error("invalid geolocation constraint %s", geocoordinate)
        # map hierarchy constraint is not empty
        elif validator.location_constraint.map_hierarchy != "":
            logger.debug("map location constraint check: constraint=%s current=%s", validator.location_constraint, lctx_location)
            if re.match(validator.location_constraint.map_hierarchy, lctx_location.map_hierarchy):
                # location is equal to  or contained within constraint
                # ie. location "Campus>Building 10" is within constraint "Campus"
                # but only if boundary is consistent
                # NOTE: constraint boundary should be "INSIDE" or "OUTSIDE"
                # lctx_location boundary will be "INSIDE" or "" (if not available)
                if validator.location_constraint.boundary == lctx_location.boundary:
                    logger.debug("location valid: inside boundary")
                    location_valid = True
                else:
                    logger.debug("location not valid: outside boundary")
                    location_valid = False
            else:
                location_valid = False
                logger.debug("location constraint did not match")
        else:
            location_valid = False
            logger.debug("no valid location constraint")

        # update validation flag in PI
        # FIXME: define location_update object and dictionary representation
        # for inter-service API
        if previous_location_valid != location_valid:
            logger.debug(
                "location_valid CHANGED: is valid? = %s\n",
                location_valid)
            validator.location_valid = location_valid
            return_dict = dict(
                pi_uuid=validator.policy_instance,
                valid=location_valid,
                location=lctx_location.get_details()
            )
            updated_validators.append(return_dict)
        elif validator.lctx_location != lctx_location:
            logger.debug(
                "location CHANGED prev=%s new=%s\n",
                validator.lctx_location,
                lctx_location)
            return_dict = dict(
                pi_uuid=validator.policy_instance,
                valid=location_valid,
                location=lctx_location.get_details()
            )
            # FIXME: add this result to notify on all location changes
            # remove it when only notify on validation changes
            updated_validators.append(return_dict)
        else:
            logger.debug(
                "location_valid NOT CHANGED: is valid? = %s\n",
                location_valid)

        # update distance in validator
        validator.location_distance = location_distance
        # update location in validator
        validator.lctx_location = lctx_location

    # Return only updated validators after checking all of them
    logger.debug("updated_validators: %s", updated_validators)

    return updated_validators


def _show_location_validators():
    logger = logging.getLogger(LogDefaults.default_log_name)

    logger.info("Location validator store:")
    try:
        validators_list = list()
        for mac, validators in location_store.validators.items():
            logger.info("MAC: %s Validators: %s", mac, validators)
            count = 0
            for validator in validators:
                logger.info("\n[%d] %s", count, validator)
                count += 1
                validator_dict_data = {}
                validator_dict_data["key"] = mac
                validator_dict_data["mc_id"] = validator.client_mc_id
                validator_dict_data["policy_instance_uuid"] = validator.policy_instance
                validator_dict_data["location_constraint"] = str(validator.location_constraint)
                validator_dict_data["lctx_location"] = str(validator.lctx_location)
                validator_dict_data["location_distance"] = validator.location_distance
                validator_dict_data["location_valid"] = validator.location_valid
                validators_list.append(validator_dict_data)
        return validators_list
    except:
        e = sys.exc_info()[0]
        print(e)
        return None


def _show_location_trackers():
    logger = logging.getLogger(LogDefaults.default_log_name)

    logger.info("Location tracker store:")
    location_trackers_list = list()
    for mac, trackers in location_store.trackers.items():
        logger.info("MAC: %s Trackers: %s", mac, trackers)
        tracker_dict_data = {}
        tracker_dict_data["key"] = mac
        tracker_dict_data["trackers"] = trackers
        location_trackers_list.append(tracker_dict_data)
    return location_trackers_list


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    meters = km * 1000.0
    return meters
