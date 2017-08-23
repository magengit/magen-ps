import os.path
import importlib.util
import threading

from magen_rest_apis.magen_app import MagenApp

__author__ = "mlipman"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"

class LocationServerUrls:
    __lock = threading.Lock()
    __instance = None

    def __init__(self):
        # lctx location server urls
        self.set_lctx_server_url_host_port("0.0.0.0")  # needs to be set to proper value before use

        # pdp server host port
        self.set_pdp_server_url_host_port("localhost:5000")  # needs to be set to proper value before use

        # Note: this is only a template, need to make sure it gets filled in properly
        self.__put_client_notification_json_body = {
            "name": "",  # Need to fill in with unique notification name
            "userId": "",  # Need to fill in with username
            "rules": [{"conditions": [
                {"condition": "locationupdate.deviceType == client"},
                # fill in with real type
                {"condition": "locationupdate.macAddressList == {}"}]}],
            # fill in macAddress
            "subscribers": [{"receivers": [
                {"uri": "http://{}/data/lctx_location_update/",
                 # fill in ip:port address
                 "messageFormat": "JSON",
                 "qos": "AT_MOST_ONCE"}]}],
            "enabled": "True",
            "enableMacScrambling": "False",
            "notificationType": "LocationUpdate"}  # fill in with real type

        self.__put_json_headers = {'content-type': 'application/json', 'accept': 'application/json',
                                   'cache-control': "no-cache"}
        self.__get_json_headers = {'accept': 'application/json'}

        # this location server
        self.__local_server_host_port = "localhost:5003"  # needs to be set to proper value before use
        self.__location_v2_url_pfx = '/magen/location/v2'
        self.__basic_auth_arguments = ('username', 'password')  # needs to be set to proper value
        self.__notification_server_userid = "userid"  # needs to be set to the proper value of the lctx server userId

    @property
    def src_version(self):
        """
        Production (default) or test mode.
        Used primarily for explicit mocking that will not be needed
        when policy unit test upgraded to use patch-style mocking.

        :return: true if production mode, false if unit test mode
        :rtype: boolean
        """
        return self.__src_version

    @src_version.setter
    def src_version(self, value):
        self.__src_version = value

    @property
    def location_v2_url_pfx(self):
        return self.__location_v2_url_pfx

    @property
    def lctx_location_server_enabled(self):
        return self.__lctx_location_server_enabled

    @property
    def get_client_location_url(self):
        return self.__get_client_location_url

    @property
    def put_client_notification_url(self):
        return self.__put_client_notification_url

    @property
    def delete_client_notification_url(self):
        return self.__delete_client_notification_url

    @property
    def put_client_notification_json_body(self):
        return self.__put_client_notification_json_body

    @property
    def get_json_headers(self):
        return self.__get_json_headers

    @property
    def put_json_headers(self):
        return self.__put_json_headers

    @property
    def basic_auth_arguments(self):
        return self.__basic_auth_arguments

    @basic_auth_arguments.setter
    def basic_auth_arguments(self, value):
        self.__basic_auth_arguments = value

    @property
    def notification_server_userid(self):
        return self.__notification_server_userid

    @notification_server_userid.setter
    def notification_server_userid(self, value):
        self.__notification_server_userid = value

    # this server's host and port
    @property
    def local_server_host_port(self):
        return self.__local_server_host_port

    @local_server_host_port.setter
    def local_server_host_port(self, value):
        self.__local_server_host_port = value

    @property
    def get_pdp_policy_instances_with_location_url(self):
        return self.__get_pdp_policy_instances_with_location_url

    @property
    def put_pdp_location_updates_url(self):
        return self.__put_pdp_location_updates_url

    @property
    def pdp_server_url_host_port(self):
        return self.__pdp_server_url_host_port

    # update location server urls 
    # if location server is 0.0.0.0 then do not connect to LCTX - only support mock updates
    def set_lctx_server_url_host_port(self, server_ip_port):
        self.__lctx_location_server_enabled = (server_ip_port != "0.0.0.0")

        self.__server_url_host_port = server_ip_port

        self.__server_base_url = "https://" + self.__server_url_host_port + "/api/"

        self.__get_client_location_url = self.__server_base_url + "location/v2/clients?macAddress={}"

        self.__put_client_notification_url = self.__server_base_url + "config/v1/notification"

        self.__delete_client_notification_url = self.__server_base_url + "config/v1/notifications/{}"

    # update pdp server urls (uses localhost always, so can't simply use server_urls)
    def set_pdp_server_url_host_port(self, pdp_server_ip_port):

        self.__pdp_server_url_host_port = pdp_server_ip_port

        self.__pdp_server_base_url = "http://" + self.__pdp_server_url_host_port + "/"

        self.__get_pdp_policy_instances_with_location_url = self.__pdp_server_base_url + "magen/policy/v2/instances/location/"

        self.__put_pdp_location_updates_url = self.__pdp_server_base_url + "data/magen_policy_instance:instances/location_updates/"

    # Putting this routine in one of a policy module imported by
    # policy_server.py rather than in policy_server.py itself gives
    # a more robust conversion from __file_ to the doc directory for
    # both the dev and installed cases.
    def location_doc_dir_set(self, app):
        """
        Set directory where policy documentation is found.
        """
        srcfile_path = os.path.abspath(__file__)
        location_root = os.path.dirname(os.path.dirname(srcfile_path)) + "/"
        if self.src_version:
           template_subfolder = 'docs/_build'
        else:
           template_subfolder = 'docs/_build'
        app.template_folder = location_root + template_subfolder

    @classmethod
    def get_instance(cls):
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = cls()
        return cls.__instance
