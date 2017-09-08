"""
Rest APIs for Magen location service interactions with an external
location service (that is source for truth for client location).

- location_lctx_rest_api.py is for rest server-side
  (e.g. event notification) interactions with the external
  location service.
- NOTE: LctxServiceApi class is for rest client-side (e.g. registration)
  interactions with the external location service.
"""

import logging
import threading
from http import HTTPStatus

from flask import Blueprint, request

# Package imports from local PIP
from magen_logger.logger_config import LogDefaults
from magen_utils_apis.singleton_meta import Singleton
from magen_rest_apis.rest_server_apis import RestServerApis

# Relative imports
from magen_location.location_apis.lctx_service_api import LctxServiceApi
from magen_location.location_libs.location_interface import LocationApi
from magen_location.location_libs.location_utils import get_url
from magen_location.location_libs.llib_policysvc import LlibPolicySvc

logger = logging.getLogger(LogDefaults.default_log_name)

location_lctx_v2 = Blueprint("location_lctx_v2", __name__)


class LctxStatistics(metaclass=Singleton):
    """
    Class to track statistics for Magen location service rest interactions
    with external location service.
    """

    def __init__(self):
        self.__lock = threading.Lock()
        self.__restApiCalls = 0
        self.__restApiEvents = 0
        self.__restApiUnknownClients = 0

    def __str__(self):
        return "{LctxStatistics: calls=%d, events=%d, unknownClients=%d}" % (
            self.__restApiCalls, self.__restApiEvents, self.__restApiUnknownClients)

    def getCalls(self):
        return self.__restApiCalls

    def incrementCalls(self):
        self.__lock.acquire(True)
        self.__restApiCalls += 1
        self.__lock.release()

    def getEvents(self):
        return self.__restApiEvents

    def incrementEvents(self):
        self.__lock.acquire(True)
        self.__restApiEvents += 1
        self.__lock.release()

    def getUnknownClients(self):
        return self.__restApiUnknownClients

    def incrementUnknownClients(self):
        self.__lock.acquire(True)
        self.__restApiUnknownClients += 1
        self.__lock.release()


@location_lctx_v2.route('/notifications/locationupdate/',
                        methods=["POST", "PUT"])
def process_lctx_location_update():
    """
    Notify Magen location service of postion updates via HTTP POST/PUT

    Invoked by external location service.

      - url - /magen/location/v2/lctx/notifications/locationupdate/
      - request.json['notifications'] - list of position updates (in external location service's expected event format).

    :return: http success/failure response with status message
    :rtype: json
    """
    lctxLocationUpdateStats = LctxStatistics()
    lctxLocationUpdateStats.incrementCalls()
    logger.debug("location update from lctx: %s\n", request)
    events = request.json["notifications"]
    prepare = "success"
    for event in events:
        macAddress = event.get("deviceId", "")
        if LocationApi.location_tracking_enabled(macAddress) is False:
            lctxLocationUpdateStats.incrementUnknownClients()
            logger.debug(
                "location tracking not enabled for macAddress=%s\n",
                macAddress)
            continue

        lctxLocationUpdateStats.incrementEvents()
        lctx_location = LctxServiceApi.process_location_update(event)

        # returns list of dicts of form {"pi_uuid": pi_uuid, "valid": valid,
        # "location": lctx_location_details}
        location_updates = LocationApi.location_update(lctx_location)
        loc_policy_svc = LlibPolicySvc()
        success, response = loc_policy_svc.do_location_updates(location_updates)

    # FIXME: handle errors on response
    return RestServerApis.respond(HTTPStatus.OK, "location update events received", prepare)


@location_lctx_v2.route('/notifications/absence/', methods=["POST", "PUT"])
def process_lctx_absence_update():
    """
    Notify Magen location service of absence updates via HTTP POST/PUT [NOT FULLY IMPLEMENTED]

      - url - /magen/location/v2/lctx/notifications/absence/
      - request.json['notifications'] - list of absence updates
        (in external location service's expected event format).
        [An absence update is where device's location is no longer
        known to the external location service.)

    :return: http success/failure response with status message
    :rtype: json
    """
    logger.debug("absence update from lctx: %s\n", request)
    events = request.json["notifications"]
    prepare = "success"
    for event in events:
        logger.debug("Event: %s\n", event)

    return RestServerApis.respond(HTTPStatus.OK, "absence update events received", prepare)


@location_lctx_v2.route('/notifications/inout/', methods=["POST", "PUT"])
def process_lctx_inout_update():
    """
    Notify Magen location service of in/out updates via HTTP POST/PUT [NOT FULLY IMPLEMENTED]

      - url - /magen/location/v2/lctx/notifications/inout/
      - request.json['notifications'] - list of location updates
        (in external location service's expected event format) for
        the case where the device has entered/left a registered
        geographic area.

    :return: http success/failure response with status message
    :rtype: json
    """
    logger.debug("inout update from lctx: %s\n", request)
    events = request.json["notifications"]
    prepare = "success"
    for event in events:
        logger.debug("Event: %s\n", event)

    return RestServerApis.respond(HTTPStatus.OK, "inout update events received", prepare)


@location_lctx_v2.route('/notifications/movement/', methods=["POST", "PUT"])
def process_lctx_movement_update():
    """
    Notify Magen location service of movement updates via HTTP POST/PUT [NOT FULLY IMPLEMENTED]

      - url - /magen/location/v2/lctx/notifications/inout/
      - request.json['notifications'] - list of location updates
        (in external location service's expected event format) for
        the case where the device has moved more than a registered
        distance from previous reported location.

    :return: http success/failure response with status message
    :rtype: json
    """
    logger.debug("movement update from lctx: %s\n", request)
    events = request.json["notifications"]
    prepare = "success"
    for event in events:
        logger.debug("Event: %s\n", event)

    return RestServerApis.respond(HTTPStatus.OK, "movement update events received", prepare)
