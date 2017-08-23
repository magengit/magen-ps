import logging
from datetime import datetime

import aniso8601
from bson.json_util import dumps
from requests.auth import HTTPBasicAuth

from magen_logger.logger_config import LogDefaults
from magen_utils_apis.datetime_api import datetime_parse_iso8601_string_to_utc, SimpleUtc

from magen_location.location_libs.location_urls import LocationServerUrls
from magen_location.location_libs.location_utils import put_url, get_url, delete_url
from magen_location.location_libs.location_storage import LocationStore

location_store = LocationStore.get_instance()


class LctxServiceApi(object):
    """
    Internal APIs wrapping Magen location service interactions with
    an external location service (that is source for truth for client
    location).

    - This class is for rest client-side (e.g. registration) interactions with the external location service.
    - NOTE: location_lctx_rest_api.py is for rest server-side (e.g. event notification) interactions with the external location service.
    """
    logger = logging.getLogger(LogDefaults.default_log_name)

    # FIXME: define a lctx_location message/response to pass back from APIs
    @staticmethod
    def process_location_update(event):
        """
        Process a device location update from an external location service.

        Intermediate step that converts external location service's
        event format into Magen location service event format.
        """
        return _process_location_update(event)

    @staticmethod
    def get_current_location(mac_address):
        """
        Poll external location service for device location.
        """
        return _get_current_location(mac_address)

    @staticmethod
    def start_location_tracking(mac_address):
        """
        Register with external location service to start tracking a device.
        """
        return _start_location_tracking(mac_address)

    @staticmethod
    def stop_location_tracking(mac_address):
        """
        Request external location servie to disable tracking of a device.
        (for which tracking was previously registered).
        """
        return _stop_location_tracking(mac_address)

    @staticmethod
    def get_location_tracker(mac_address):
        """
        Return internal handle for a device tracking registration with an
        external location service.

        This handle is created as a side-effect of start_location_tracking().
        The handle is used externally as a boolean indicator that
        the external service is tracking location.
        """
        return location_store.get_tracker(_get_tracker_key(mac_address))


def _get_tracker_key(mac_address):
    return "LCTX:" + mac_address


def _process_location_update(event):
    LctxServiceApi.logger.debug("process_location_update for %s\n", event)

    # construct lctx_location dict
    lctx_location = dict()
    # FIXME: should define set of notification types and check them in the update function
    # Support inout, absence and other notifications
    # FIXME: Reinaldo: This assert breaks the location test. In the current JSOn messages
    # FIXME: Reinaldo: the notifcationType is 'inout'
    # assert event["notificationType"] == "locationupdate"
    lctx_location["notificationType"] = event["notificationType"]
    lctx_location["deviceId"] = event["deviceId"]
    lctx_location["locationCoordinate"] = event["locationCoordinate"]
    lctx_location["geoCoordinate"] = event["geoCoordinate"]
    lctx_location["locationMapHierarchy"] = event["locationMapHierarchy"]
    # Note: assuming the event has a boundary specification
    # if not specified in the event, default to "INSIDE" - assumption here is that
    # a location event without boundary is a location update (where the client is)
    # this will match the constraint right now (since it is always INSIDE)
    lctx_location["boundary"] = event.get("boundary", "INSIDE")

    # Note: convert example of how to generate a date string and then parse it back into a datetime object
    # policy_session_entity.setdefault("testdate", aniso8601.parse_datetime(datetime.utcnow().
    # replace(tzinfo=SimpleUtc()).isoformat()))
    location_last_time = event["lastSeen"]
    if location_last_time:
        utc_time = datetime_parse_iso8601_string_to_utc(location_last_time)
        lctx_location["lastLocated"] = utc_time.isoformat()

    lctx_location["creationTimestamp"] = datetime.utcnow().replace(tzinfo=SimpleUtc()).isoformat()

    return lctx_location


def _get_current_location(mac_address):
    # NOTE: we protect update of validators from async notification through
    # Rest Apis using thread locks in location_storage.py
    LctxServiceApi.logger.debug("get current location for mac=%s\n", mac_address)
    server_urls_instance = LocationServerUrls.get_instance()

    lctx_location = {}
    # only update LCTX if enabled
    if server_urls_instance.lctx_location_server_enabled:
        server_urls_instance = LocationServerUrls.get_instance()
        auth = HTTPBasicAuth(*server_urls_instance.basic_auth_arguments)
        headers = server_urls_instance.get_json_headers
        success, response = get_url(server_urls_instance.get_client_location_url.format(
            mac_address), auth=auth, verify=False, headers=headers)

        if success:
            LctxServiceApi.logger.debug(
                "found tracking info for client mac=%s resp=%s",
                mac_address,
                response)
            assert len(response) == 1, "expected list of length 1"
            response = response[0]
            # FIXME: should define set of notification types
            lctx_location["notificationType"] = "_initialLocationGet"
            if response.get("macAddress", "") != mac_address:
                LctxServiceApi.logger.error(
                    "macAddresses do not match %s != %s", response.get(
                        "macAddress", ""), mac_address)
            lctx_location["deviceId"] = mac_address
            lctx_location["locationCoordinate"] = response.get(
                "mapCoordinate", {})
            lctx_location["geoCoordinate"] = response.get(
                "geoCoordinate", {})
            mapInfo = response.get("mapInfo", {})
            # get the initial map hierarchy
            lctx_location["locationMapHierarchy"] = mapInfo.get("mapHierarchyString", "")
            # if map hierarchy or geocoordinate defined then assume boundary is "INSIDE"
            # Note: we don't get a boundary with the initial get - its a location
            if lctx_location["locationMapHierarchy"] !=  "" or lctx_location["geoCoordinate"] != {}:
                lctx_location["boundary"] = "INSIDE"
            else:
                lctx_location["boundary"] = ""

            statistics = response.get("statistics", None)
            if statistics:
                location_last_time = statistics.get("lastLocatedTime", None)
                if location_last_time:
                    location_last_time_utc = aniso8601.parse_datetime(location_last_time).replace(tzinfo=SimpleUtc()).isoformat()
                    lctx_location["lastLocated"] = location_last_time_utc

            lctx_location["creationTimestamp"] = datetime.utcnow().replace(tzinfo=SimpleUtc()).isoformat()

            return lctx_location

    # if lctx not enabled or we get an error from getting client location then return empty lctx_location
    # update location so we don't allow unauthorzied access to files
    LctxServiceApi.logger.debug("did not find tracking info for client mac=%s", mac_address)
    # FIXME: should define set of notification types
    lctx_location["notificationType"] = "_initialLocationGet"
    lctx_location["deviceId"] = mac_address
    lctx_location["locationCoordinate"] = {}
    lctx_location["geoCoordinate"] = {}
    lctx_location["locationMapHierarchy"] = ""
    lctx_location["boundary"] = ""
    lctx_location["creationTimestamp"] = datetime.utcnow(
    ).replace(tzinfo=SimpleUtc()).isoformat()

    return lctx_location

# NOTE: this can also work on a list of location updates


def _start_location_tracking(mac_address):
    # NOTE: we protect update of validators from async notification through
    # Rest Apis using thread locks in location_storage.py
    LctxServiceApi.logger.debug("start location tracking for mac=%s\n", mac_address)
    server_urls_instance = LocationServerUrls.get_instance()

    # only update LCTX if enabled
    if server_urls_instance.lctx_location_server_enabled:
        notification_name = "Magen-notification-" + mac_address.replace(":", "-")
        # FIXME: get this from an environment variable or figure it out
        # dynamically at runtime
        notification_ip_port = server_urls_instance.local_server_host_port
        notification_user_id = server_urls_instance.notification_server_userid

        # FIXME: what happens if notification already registered ?
        # should we do a get first to check and then not re-register ?
        # Treat json body as a template
        notification_type = "LocationUpdate"  # can be changed for other types
        notification_type_lower = notification_type.lower()
        notification_json_body = server_urls_instance.put_client_notification_json_body
        notification_json_body["name"] = notification_name
        notification_json_body["userId"] = notification_user_id

        notification_condition0 = "{}.deviceType == client".format(
            notification_type_lower)
        notification_condition1 = "{}.macAddressList == {};".format(
            notification_type_lower, mac_address)
        # Note: Uri is dependent on notification type string - make sure URIs
        # match
        notification_uri = "http://{}/data/lctx_{}_update/".format(
            notification_ip_port, notification_type_lower)

        notification_json_body["notificationType"] = notification_type
        notification_json_body["rules"][0]["conditions"][
            0]["condition"] = notification_condition0
        notification_json_body["rules"][0]["conditions"][
            1]["condition"] = notification_condition1
        notification_json_body["subscribers"][0][
            "receivers"][0]["uri"] = notification_uri

        notification_json_string = dumps(notification_json_body)
        LctxServiceApi.logger.debug(
            "start LCTX location tracking: JSON string = %s",
            notification_json_string)
        auth = HTTPBasicAuth(*server_urls_instance.basic_auth_arguments)
        headers = server_urls_instance.put_json_headers
        success, response = put_url(server_urls_instance.put_client_notification_url,
                                    notification_json_string, auth=auth, verify=False, headers=headers)

        if success:
            LctxServiceApi.logger.debug(
                "LCTX start location tracking succeeded: response=%s",
                response)
            location_store.add_tracker(
                _get_tracker_key(mac_address), [notification_name, notification_type])
            return True
        else:
            LctxServiceApi.logger.debug(
                "LCTX start location tracking failed: response=%s",
                response)
            return False

    return True


def _stop_location_tracking(mac_address):
    # NOTE: we protect update of validators from async notification through
    # Rest Apis using thread locks in location_storage.py
    LctxServiceApi.logger.debug("stop location tracking for mac=%s\n", mac_address)
    server_urls_instance = LocationServerUrls.get_instance()

    # only update LCTX if enabled
    if server_urls_instance.lctx_location_server_enabled:
        notification_name = "Magen-notification-" + mac_address.replace(":", "-")
        auth = HTTPBasicAuth(*server_urls_instance.basic_auth_arguments)
        headers = server_urls_instance.put_json_headers
        url = server_urls_instance.delete_client_notification_url.format(
            notification_name)

        success, response = delete_url(
            url, json_req=None, auth=auth, verify=False, headers=headers)

        if success:
            LctxServiceApi.logger.debug(
                "LCTX stop location tracking succeeded: response=%s",
                response)
            location_store.remove_tracker(_get_tracker_key(mac_address))
            return True
        else:
            LctxServiceApi.logger.error(
                "LCTX stop location tracking failed: response=%s",
                response)
            return False

    return True
