import sys
import time
import logging
from http import HTTPStatus

import flask
from flask import request
from requests.auth import HTTPBasicAuth

from magen_logger.logger_config import LogDefaults
from magen_rest_apis.rest_server_apis import RestServerApis

from magen_location.location_libs.location_urls import LocationServerUrls
from magen_location.location_libs.location_interface import LocationApi
from magen_location.location_libs.location_dbthread import \
    LocDb, _ls_spawn_database_update_thread
from magen_location.location_libs.location_utils import get_url

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"

location_v2 = flask.Blueprint("location_v2", __name__)
location_tracking = flask.Blueprint("location_tracking", __name__)
logger = logging.getLogger(LogDefaults.default_log_name)


@location_v2.route('/client/<mac>/', methods=["GET"])
def process_get_client_location(mac):
    """
    Retrieve a device's location information (via HTTP GET)

      - url - /magen/location/v2/<mac>/

    :param mac: device mac address
    :type mac: mac address string
    :return: http success/failure response with status message
    :rtype: json
    """
    location_urls = LocationServerUrls.get_instance()
    auth = HTTPBasicAuth(*location_urls.basic_auth_arguments)
    headers = location_urls.get_json_headers
    success, response = get_url(location_urls.get_client_location_url.format(
        mac), auth=auth, verify=False, headers=headers)

    if success:
        return RestServerApis.respond(HTTPStatus.OK, "get_client_location", {
            "success": True, "cause": response})
    else:
        return RestServerApis.respond(HTTPStatus.INTERNAL_SERVER_ERROR,
                                      "get_client_location", {
                                          "success": False, "cause": response})


@location_v2.route('/stores/', methods=["GET"])
def show_location_validators():
    """
    Retrieve cached location information for all (via HTTP GET)

      - url - /magen/location/v2/stores/

    Return location information held by Magen location service, without
    triggering transitive operation to external location service.

    :return: http success/failure response with list of location information
    :rtype: json
    """
    try:
        location_validators_list = LocationApi.show_location_validators()
        location_trackers_list = LocationApi.show_location_trackers()

        # This doesn't work in Python 3.4 - which is what we have in Ubuntu dockers
        # composed_dict = { **location_validators_list, **location_trackers_list }
        # Until we move fully to Python 3.5.1
        # composed_dict = location_validators_list.copy()
        # composed_dict.update(location_trackers_list)

        # creating a new dictionary with separate keys for validators and lctx_trackers
        # Note: the previous problem with JSONify was due to the lctx trackers
        # containing a set as a key value (changed it to a list)
        composed_dict = {}
        if location_validators_list or location_trackers_list:
            composed_dict["validators"] = location_validators_list
            composed_dict["trackers"] = location_trackers_list

        result = {
            "success": True,
            "location_stores": composed_dict,  # can be empty
            "cause": None}
        return RestServerApis.respond(HTTPStatus.OK, "GET Location Stores",
                                      result)
    except TypeError as e:
        e = sys.exc_info()[0]
        print(e)


# Note: remove internal state, does not cleanup LCTX state

@location_v2.route('/stores/', methods=["DELETE"])
def delete_location_validators():
    """
    Delete cached location information for all (via HTTP DELETE)

      - url - /magen/location/v2/stores/

    :return: http success/failure response with list of location information
    :rtype: json
    """
    LocationApi.clear_location_validators()
    LocationApi.clear_location_trackers()
    return RestServerApis.respond(HTTPStatus.OK, "location_clear_stores",
                                  "success")


@location_v2.route('/notifications/', methods=["POST", "PUT"])
def process_events():
    """
    Announce location update events (via HTTP POST/PUT). [NOT YET IMPLEMENTED.]

      - url - /magen/location/v2/notifications/
      - request.json['notifications'] - list of events

    :return: http success/failure response with list of location information
    :rtype: json
    """
    events = request.json["notifications"]
    prepare = "success"
    for event in events:
        logger.info("Event: %s\n", event)
        logger.info("Device: %s\n", event["deviceId"])

    return RestServerApis.respond(HTTPStatus.OK, "events received", prepare)


@location_v2.route('/tracking/', methods=["POST", "PUT"])
def register_location_tracking():
    """
    Enable location tracking for supplied device with Magen location service (via HTTP POST/PUT).

      - url - /magen/location/v2/tracking/
      - request.json['pi_uuid'] - policy (location client) handle on device to track
      - request.json['client_info'] - info, including mac_address, on device to track

    :return: http success/failure response with list of location information
    :rtype: json
    """

    logger.info(
        "register location tracking from pdp: %s %s\n",
        request,
        request.json)
    prepare = "success"
    req = request.json
    # FIXME: define API message for argument passing {pi_uuid, client_info, location_constraint}
    # pull out info into only fields that are necessary at top level - no embedded objects/messages if at all possible
    # if fields don't exist, do the reasonable thing - deal with the data you get
    # { pi_uuid, mc_id, location_map_hierarchy }
    pi_uuid = req["pi_uuid"]
    macAddress = req["client_info"]["mac_address"]
    # initiate location tracking in local server
    if LocationApi.start_location_tracking(
            pi_uuid,
            req["client_info"],
            req["location_constraint"]):
        # add the macAddress to the list of macAddresses to update location
        # this will get current location and update the PDP properly
        # it will also update LCTX if not already updated
        LocDb.databaseSignal.lock.acquire(True)
        LocDb.databaseSignal.update_tracking_addresses.add(macAddress)
        LocDb.databaseSignal.lock.release()

        return RestServerApis.respond(HTTPStatus.OK,
                                      "register location tracking", prepare)
    else:
        logger.info(
            "register location tracking from pdp failed: pi_uuid=%s mac=%s",
            pi_uuid,
            macAddress)
        prepare = "failure, pi_uuid=%s mac=%s" % (pi_uuid, macAddress)
        return RestServerApis.respond(HTTPStatus.NOT_FOUND,
                                      "register location tracking", prepare)


@location_v2.route('/tracking/', methods=["DELETE"])
def deregister_location_tracking():
    """
    Disable location tracking for supplied device with Magen location service (via HTTP DELETE).

    (Assumption is that location tracking for supplied device was previously registered with Magen locaiton service.)

      - url - /magen/location/v2/tracking/
      - request.json['pi_uuid'] - policy (location client) handle on device to track
      - request.json['client_info'] - info, including mac_address, on device to track

    :return: http success/failure response with list of location information
    :rtype: json
    """
    logger.info(
        "deregister location tracking from pdp: %s %s\n",
        request,
        request.json)
    req = request.json
    # FIXME: define API object for argument passing {pi_uuid, client_info}
    pi_uuid = req["pi_uuid"]
    # stop location tracking in local server
    macAddress = req["client_info"]["mac_address"]
    mc_id = req["client_info"]["mc_id"]
    if LocationApi.stop_location_tracking(
            macAddress,
            mc_id=mc_id,
            pi_uuid=pi_uuid):
        prepare = "success"
        # add the macAddress to the list of macAddresses to update location
        # it will stop lctx location tracking if this was the last one - put on
        # update thread
        LocDb.databaseSignal.lock.acquire(True)
        LocDb.databaseSignal.update_tracking_addresses.add(macAddress)
        LocDb.databaseSignal.lock.release()
        return RestServerApis.respond(HTTPStatus.OK,
                                      "deregister location tracking", prepare)
    else:
        logger.info(
            "deregister location tracking from pdp failed: mac=%s",
            macAddress)
        prepare = "failure, %s not found" % macAddress
        return RestServerApis.respond(HTTPStatus.NOT_FOUND,
                                      "deregister location tracking", prepare)

@location_v2.route('/database_update_thread/start/',
                         methods=["POST", "PUT"])
def process_start_database_update_thread():
    """...
    Enable database update task (via HTTP POST/PUT).

      - url - /magen/location/v2/database_update_thread/start/

    :return: http success/failure response with status message
    :rtype: json
    """

    if LocDb.databaseUpdateThread is not None:
        return RestServerApis.respond(
            HTTPStatus.INTERNAL_SERVER_ERROR, "start_database_update_thread", {
                "success": False, "cause": "thread already running"})
    else:
        _ls_spawn_database_update_thread("Rest API")
        return RestServerApis.respond(HTTPStatus.OK, "start_database_update_thread",
                                      {"success": True, "cause": "thread started"})


@location_v2.route('/database_update_thread/stop/',
                   methods=["POST", "PUT"])
def process_stop_database_update_thread():
    """
    Disable database update background task (via HTTP POST/PUT).

      - url - /magen/location/v2/database_update_thread/stop/

    :return: http success/failure response with status message
    :rtype: json
    """

    if LocDb.databaseUpdateThread is None:
        return RestServerApis.respond(
            HTTPStatus.INTERNAL_SERVER_ERROR, "stop_database_update_thread", {
                "success": False, "cause": "thread not running"})
    else:
        LocDb.databaseSignal.go = False
        # wait for thread to exit
        LocDb.databaseUpdateThread.join()

        # Reset signal and thread
        LocDb.databaseSignal = None
        LocDb.databaseUpdateThread = None

        return RestServerApis.respond(HTTPStatus.OK, "stop_database_update_thread",
                                      {"success": True, "cause": "thread stopped"})


@location_v2.route('/database_update_thread/test/<iterations>/',
                   methods=["POST", "PUT"])
def process_test_thread_counter(iterations):
    """
    Generate test load on location service (via HTTP POST/PUT).

      - url - /magen/location/v2/database_update_thread/test/<iterations>/

    :param iterations: integer count of test interations to execute
    :type iterations: integer string
    :return: http success/failure response with status message
    :rtype: json
    """

    if LocDb.databaseSignal is None:
        return RestServerApis.respond(
            HTTPStatus.INTERNAL_SERVER_ERROR, "test_thread_counter", {
                "success": False, "cause": "test thread not running"})

    # cast to int
    iterations = int(iterations)

    # set flag to thread to do thread lock test
    LocDb.databaseSignal.testIterations = iterations
    LocDb.databaseSignal.testType = 'testCounter'
    LocDb.databaseSignal.testArg = request.json

    while not LocDb.databaseSignal.testStarted:
        time.sleep(.01)

    logger.debug(
        "test_thread_counter: test started %d iterations", iterations)

    # reset flag - only one iteration should run
    LocDb.databaseSignal.testIterations = 0
    LocDb.databaseSignal.testStarted = False

    startTime = time.time()
    for i in range(iterations):
        LocDb.testCounterFlask.count += 1
        LocDb.testCounterCombined.lock.acquire(True)
        LocDb.testCounterCombined.count += 1
        LocDb.testCounterCombined.lock.release()
    endTime = time.time()

    sumCounts = LocDb.testCounterFlask.count + LocDb.testCounterThread.count
    combinedCounts = LocDb.testCounterCombined.count
    totalSecs = endTime - startTime

    logger.debug(
        "test_thread_counter: flask=%s thread=%s flask+thread=%s combined=%s\n",
        LocDb.testCounterFlask.count,
        LocDb.testCounterThread.count,
        sumCounts,
        combinedCounts)

    return RestServerApis.respond(HTTPStatus.OK, "test_thread_counter", {
        "success": True, "cause": "counters incremented in %s secs: sum=%s combined=%s" %
        (totalSecs, sumCounts, combinedCounts)})


