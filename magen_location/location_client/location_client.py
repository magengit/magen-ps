#! /usr/bin/python3

import logging
from json import dumps

from magen_logger.logger_config import LogDefaults
from magen_rest_apis.server_urls import ServerUrls

from magen_location.location_libs.location_utils import put_url, delete_url
from policy.mongo_apis.mongo_policy_instance_api import MongoPolicyInstanceApi


# FIXME: define common API objects for register and deregister functions
# {pi, client_info, location_constraint}
# {pi, client_info}

# This file is part of PDP and not Location server. It is the interface that PDP
# uses to communicate with Location Server


class LocationClientApi(object):
    """
    Library exported by Magen location service, wrapping client side calls to rest APIs exported by Magen location service.

    - Magen policy service is an example users of this module.
    - Note that Magen location service itself is an adaptation service that communicates with external location service(s) that are (or at least are closer to) location source of truth
      - off-loads the complexity of managing those external interactions from clients
      - limits the number of Magen clients of those external services to one

    Tracking is, at the option of Magen location service and based on the capabilies of external location service, subject to the supplied constraints, e.g. policy may only need to know if device enters/leaves an area relevant to a policy, not about movement between points inside the area or between points outside the area.
    """

    _logger = logging.getLogger(LogDefaults.default_log_name)

    @staticmethod
    def register_location_tracking(pi_uuid, client_info, location_constraint):
        """
        Register supplied device with Magen location service, to have its location tracked, as per class documentation.

        :param pi_uuid:
        :param client_info: additional device information for location service to identify device to external location service
        :param location_constraint: higher-level representation of constraint, to allow optimization of event updating
        :type pi_uuid: uuid
        :type client_info: json dict
        :type location_constraint: json dict
        :return: success: success/failure indication
        :return response: rest response to underlying PUT to location service
        :rtype success: bool
        :rtype response: json
        """
        if isinstance(location_constraint, dict) and isinstance(client_info, dict):
            LocationClientApi._logger.debug("register location tracking: pi=%s client_info=%s location_constraint=%s",
                         pi_uuid, client_info, location_constraint)
            # call out to location server to register PI
            json_body = dict(pi_uuid=pi_uuid, client_info=client_info, location_constraint=location_constraint)
            server_urls = ServerUrls.get_instance()
            success, response = put_url(server_urls.location_server_base_url + "tracking/",
                                        dumps(json_body))
            return success, response
        else:
            raise TypeError("dictionaries expected")

    @staticmethod
    def check_and_register_location_tracking(policy_contract_dict, policy_instance_list):
        """
        Register supplied devices (which are subject to supplied policy contract) with Magen location service, to have their location tracked, as per class documentation.

        :param policy_contract_dict: supplied to determine if location constraints apply to this policy, i.e. for "check" portion of functionality
        :param policy_instance_list: list of policy instances, needed to provide pi_uuid, client_info, and location constraint info
        :type policy_contract_dict: dictionary
        :type policy_instance_list: list of dictionaries
        :return: success: success/failure indication
        :return response: rest response to underlying PUT to location service
        :rtype success: bool
        :rtype response: json
        """
        if policy_contract_dict.get("location_name", None) is not None:
            for policy_instance_dict in policy_instance_list:
                success, response = LocationClientApi.register_location_tracking(
                    policy_instance_dict["uuid"], policy_instance_dict["client_info"], policy_instance_dict["location_constraint"])
                if not success:
                    msg = "Failed to register location tracking for PI: {}".format(policy_instance_dict)
                    LocationClientApi._logger.error(msg)
                    return False, msg
        return True, "Location tracking registration successful"


    @staticmethod
    def deregister_all_location_tracking():
        """
        Deregister all device tracking previously registered with Magen location service.

        :return: success: success/failure indication
        :return response: rest response to underlying PUT to location service
        :rtype success: bool
        :rtype response: json
        """
        server_urls = ServerUrls.get_instance()
        success, msg = delete_url(server_urls.location_stores_url)
        return success, msg

    @staticmethod
    def deregister_many_location_tracking(pi_uuid_list):
        """
        Deregister device tracking previously registered with Magen location service, based on supplied list of devices.

        :param pi_uuid_list: list of pi_uuids. (pi_uuid is sufficient to for Magen location service to identify a previously registered tracking request.)
        :type pi_uuid: list of uuids
        :return: success: success/failure indication
        :return response: rest response to underlying PUT to location service
        :rtype success: bool
        :rtype response: json
        """
        for pi_uuid in pi_uuid_list:
            db_return = MongoPolicyInstanceApi.get_policy_instance(pi_uuid)
            policy_instance_dict = db_return.documents
            success, response = LocationClientApi.deregister_location_tracking(pi_uuid, policy_instance_dict["client_info"])
            if not success:
                # If one fails we stop right there. We can change this later.
                return success, response
        return True, "All location tracking stopped"

    @staticmethod
    def deregister_location_tracking(pi_uuid, client_info):
        """
        Deregister device tracking previously registered with Magen location service, based on supplied device identification.

        :param pi_uuid: identification of device previously registered for tracking with Magen location service
        :param client_info: additional device information for location service to identify device to external location service
        :type pi_uuid: uuid
        :type client_info: json dict
        :return: success: success/failure indication
        :return response: rest response to underlying PUT to location service
        :rtype success: bool
        :rtype response: json
        """
        LocationClientApi._logger.debug("deregister location tracking: pi=%s", pi_uuid)
        # call out to location server to deregister PI
        json_body = dict(pi_uuid=pi_uuid, client_info=client_info)
        server_urls = ServerUrls.get_instance()
        success, response = delete_url(server_urls.location_server_base_url + "tracking/",
                                       dumps(json_body))
        return success, response

    # NOTE: this is currently implemented by getting the current_location from the PI in the PDP database
    # Stub left here in case we want to go to location server to get the info
    @staticmethod
    def get_current_location(pi_uuid):
        """
        Retrieve device location for indicated device from Magen location service. [NOT YET IMPLEMENTED.]

        :param pi_uuid: identification of device previously registered for tracking with Magen location service
        :type pi_uuid: uuid
        :return: location information
        :rtype: dict
        """
        LocationClientApi._logger.debug("get current location: pi=%s", pi_uuid)
        # FIXME: call out to location server to get the current location
        # success, response = get_url(location_server_url_base + "client/" + mac)
        # FIXME: add json body to get request

        assert False, "Function not implemented - see PolicyInstanceApi.get_location"
        return True, "Not Implemented"

        # Unreachable code
        # if success:
        #     map_hierarchy = response["map_hierarchy"]
        #     location = map_hierarchy.split(">")
        #     return True, location
        # else:
        #     return False, response
