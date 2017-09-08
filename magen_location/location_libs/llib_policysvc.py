import logging
from bson.json_util import dumps

from magen_logger.logger_config import LogDefaults
from magen_utils_apis.singleton_meta import Singleton

from magen_location.location_libs.location_urls import LocationServerUrls
from magen_location.location_libs.location_utils import put_url

__author__ = "gibson@cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"

logger = logging.getLogger(LogDefaults.default_log_name)


class LlibPolicySvc(metaclass=Singleton):
    """
    Interface wrapper for location talking to policy service
    """

    def do_location_updates(self, location_updates):
        """
        Call out to PDP to update location_valid and current_location fields
        in PI
        """
        logger.debug("location_updates: %s\n", location_updates)
        location_urls = LocationServerUrls.get_instance()
        pdp_location_updates_url = location_urls.put_pdp_location_updates_url
        jsonBody = dict(location_updates=location_updates)
        success, response = put_url(pdp_location_updates_url, dumps(jsonBody))
        if not success:
            logger.error(
                "pdp server returned error on location updates: %s",
                response)

        return success, response
