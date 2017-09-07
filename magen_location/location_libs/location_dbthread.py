from functools import wraps
import logging
import threading
import time
from datetime import datetime
from uuid import *

import flask
from flask import request
from flask.json import JSONEncoder
from flask_cors import CORS
from requests.auth import HTTPBasicAuth
from pathlib import Path

from magen_logger.logger_config import LogDefaults
from magen_logger.logger_config import initialize_logger
from magen_utils_apis.datetime_api import SimpleUtc

from magen_location.location_libs.location_utils import get_url
from magen_location.location_libs.location_urls import LocationServerUrls
from magen_location.location_libs.location_interface import LocationApi
from magen_location.location_libs.llib_policysvc import LlibPolicySvc
from magen_location.location_apis.lctx_service_api import LctxServiceApi
from magen_location.location_server.location_lctx_rest_api import LctxStatistics

__author__ = "mlipman"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"

logger = logging.getLogger(LogDefaults.default_log_name)

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                # print(str(obj))
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

class Signal:
    go = True  # set to False to cause thread to exit
    testIterations = 0  # set to >0 to enable
    testStarted = False  # set true when thread starts test
    testType = None
    testArg = {}
    lock = threading.Lock()
    update_tracking_addresses = set()
    retry_tracking_addresses = set()


class Counter:
    count = 0
    lock = threading.Lock()


# thread safe statistics class
# writes are protected
# reads are not, but don't need to be


class LocDb:
    databaseSignal = None
    databaseUpdateThread = None

    testCounterFlask = Counter()
    testCounterThread = Counter()
    testCounterCombined = Counter()


def _ls_timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        logger.warning("@timefn:" + fn.__name__ +
                       " took " + str(t2 - t1) + " seconds")
        return result

    return measure_time


def _ls_do_counter_test(iterations):
    # test thread locking
    # NOTE: it is necessary - threads do run concurrently
    # acquiring locks takes about 2x the time as not doing the locking
    for i in range(iterations):
        LocDb.testCounterThread.count += 1
        LocDb.testCounterCombined.lock.acquire(True)
        LocDb.testCounterCombined.count += 1
        LocDb.testCounterCombined.lock.release()

    return True


# Location service architecture
# 1. Listen on message bus for Location Policy instantiations -OR-
# 2. Query database for all PIs with location, use PI creation timestamp to track
# 3. Request notifications from LCTX, listen for notifications from LCTX
# 4. GET current location from LCTX for new PIs
#    Use thread to do the GET ? or just do a sync request to LCTX
# 5. Separate thread for notification processing ?
#
# 2 threads:
# one for web service callback on notifications - main()
# one for monitoring bus/monitoring database changes - database_update()
#
# This could be the way we do time tracking as well - query magen_mongo for time validity expiration and then update next time check
# and update the time_valid_flag in the PI so it can be used to answer re-validation requests from client
#
def _ls_spawn_database_update_thread(caller):
    assert LocDb.databaseSignal is None and LocDb.databaseUpdateThread is None, "database update thread is already initialized"

    logger.debug("spawning database update thread...\n")

    LocDb.databaseSignal = Signal()
    LocDb.databaseUpdateThread = threading.Thread(
        target=_ls_database_update_thread, args=(
            caller, LocDb.databaseSignal))
    LocDb.databaseUpdateThread.start()

    return True


def _ls_database_update_thread(caller, signal):
    """
    Query database for all PIs with location, use PI creation timestamp to track
    Request notifications from LCTX, listen for notifications from LCTX
    GET current location from LCTX for new PIs
    """

    timeNow = datetime.utcnow().replace(tzinfo=SimpleUtc())
    lastTime = datetime.fromtimestamp(0).replace(tzinfo=SimpleUtc())
    logger.info(
        "database_update_thread: called by %s starting at %s..." %
        (caller, timeNow))
    # location_urls = LocationServerUrls.get_instance()

    # test whether thread locks are needed
    lctxLocationUpdateStats = LctxStatistics()

    while True:
        if not signal.go:
            logger.info("database_update_thread signal.go=False, exiting...\n")
            break

        timeNow = datetime.utcnow().replace(tzinfo=SimpleUtc())

        policiesFound = 0

        clientMacAddresses = set()

        # Note: first walk the list of PIs and initiate location tracking on all of them
        # store up the unique macAddresses in a set and then iterate over the set getting the current location of each client
        # this will avoid redundant (expensive) calls to getting the client
        # location from LCTX

        # use the creation timestamp to find new PIs
        # FIXME: Call out to PDP to get PIs to track
        # Every second check location validators to update if not updated or not updated recently
        # PDP will register location info with location server
        # Every five minutes - get all outstanding PIs - mark and sweep -
        # create/remove location trackers
        location_urls = LocationServerUrls.get_instance()

        pdp_policy_instances_with_location_url = location_urls.get_pdp_policy_instances_with_location_url + \
            lastTime.isoformat() + "/"
        success, response = get_url(pdp_policy_instances_with_location_url)

        if not success:
            logger.error("pdp server returned error: (%s => %s).  Keeping lastTime=%s", pdp_policy_instances_with_location_url, response, lastTime)
            policy_instances = list()
            # keep lastTime the same so we get all new policies when PDP is up again
        else:
            policy_instances = response['response']
            # update last time as now
            lastTime = timeNow

        # FIXME: the location constraint comes from the policy instance
        # need to deal with changes to PIs and constraints
        # if updates occur - then PIs must re-register with location service
        # or change their creation timestamp so new update will occur
        if policy_instances:
            logger.info("policy_instances: %s", policy_instances)

        for policy_instance in policy_instances:
            logger.debug("initiate_location_tracking: pi=%s", policy_instance)
            # FIXME: define policy_instance_info message that represents {pi_uuid, client_info, location_constraint}
            # this is the same object passed in from the register location tracking API
            # this should also be all top level and only fields necessary
            pi_uuid = policy_instance["uuid"]

            # if not already tracking policy, then start tracking (add validator and lctx tracker)
            # this could happen on a location server restart
            client_info = policy_instance["client_info"]
            # Note: We currently use whatever is passed in as the "mac_address" to track the client
            # this could be mac, IP or even client UUID (in case of box web app)
            # if not a real mac_address then LCTX won't be able to track it for now
            # FIXME: separate tracking db key from mac/ip or other LCTX address
            macAddress = client_info["mac_address"]
            if LocationApi.get_current_location_constraint(pi_uuid, macAddress) == {}:
                location_constraint = policy_instance["location_constraint"]
                LocationApi.start_location_tracking(
                    pi_uuid,
                    client_info,
                    location_constraint)
                # Start LCTX tracking locations for newly added macAddresses
                clientMacAddresses.add(macAddress)
                # update overall policies found
                policiesFound += 1

        # Now walk the unique clients and update the current location
        uniqueClientsFound = len(clientMacAddresses)
        if uniqueClientsFound > 0:
            logger.info(
                "update tracking for all unique clients: %s",
                clientMacAddresses)

        # get current location of new PIs being tracked and update PIs
        # add in addresses for PDP registered PIs
        trackingClientMacAddresses = set()
        # add database found macs from loop above
        trackingClientMacAddresses.update(clientMacAddresses)
        # add retry macs from previous loop
        trackingClientMacAddresses.update(signal.retry_tracking_addresses)
        # grab updates from PDP
        signal.lock.acquire(True)
        trackingClientMacAddresses.update(
            signal.update_tracking_addresses)  # add PDP registered macs
        # re-initialize for next loop
        signal.update_tracking_addresses = set()  # re-initialize for next loop
        signal.retry_tracking_addresses = set()  # re-initialize for next loop
        signal.lock.release()
        if len(trackingClientMacAddresses) > 0:
            logger.info(
                "update tracking for all unique clients: %s",
                clientMacAddresses)

        for macAddress in trackingClientMacAddresses:
            tracking_local_location = LocationApi.location_tracking_enabled(
                macAddress)
            tracking_lctx_location = LctxServiceApi.get_location_tracker(
                macAddress)

            # Only try to update LCTX if it is enabled (not 0.0.0.0)
            if location_urls.lctx_location_server_enabled:

                # if macAddress is being tracked locally then try to get current
                # location from LCTX and update PDP
                if tracking_local_location:
                    lctx_location = LctxServiceApi.get_current_location(macAddress)
                    # update location validators
                    location_updates = LocationApi.location_update(lctx_location)
                    loc_policy_svc = LlibPolicySvc()
                    success, response = loc_policy_svc.do_location_updates(
                        location_updates)
                    if not success:
                        logger.error("pdp location updates failed: %s", response)
                        signal.retry_tracking_addresses.update(macAddress)

                # now update LCTX automatic tracking - start or stop
                if tracking_local_location and not tracking_lctx_location:
                    success = LctxServiceApi.start_location_tracking(macAddress)
                    if not success:
                        logger.error(
                            "start location tracking failed for mac=%s",
                            macAddress)
                        signal.retry_tracking_addresses.update(macAddress)
                elif not tracking_local_location and tracking_lctx_location:
                    success = LctxServiceApi.stop_location_tracking(macAddress)
                    if not success:
                        logger.error(
                            "stop location tracking failed for mac=%s", macAddress)
                        signal.retry_tracking_addresses.update(macAddress)

        # FIXME: every minute or so scan the location tracker database to age out PIs that no longer exist
        # garbage collect - mark and sweep against PDP PIs (using mark timestamp to avoid removing new PIs)
        # If last PI for MAC address - removal should also stop LCTX tracking
        # Needs to be thread safe

        logger.debug(
            "database_update_thread: %d policy instances updated, %d unique clients found" %
            (policiesFound, uniqueClientsFound))
        logger.debug(
            "database_update_thread: locationUpdateStats=%s\n" %
            lctxLocationUpdateStats)

        # test thread locking - caller will set the iteration count, then reset once it sees thread started flag set
        # so read iterations once and store it locally
        iterations = signal.testIterations
        if iterations > 0:
            signal.testStarted = True
            if signal.testType == 'testCounter':
                logger.info(
                    "database_update_thread: testCounter: %d test iterations" %
                    iterations)
                _ls_do_counter_test(iterations)
                signal.testIterations = 0
            else:
                logger.error(
                    "database_update_thread: invalid test type=%s",
                    signal.testType)

        # sleep 1 second
        time.sleep(1)

    logger.debug("Exiting database update thread\n")
    return True
