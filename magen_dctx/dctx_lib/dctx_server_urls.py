from magen_utils_apis.singleton_meta import Singleton
from magen_rest_apis.server_urls import ServerUrls

__author__ = "gibson@cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"


class DctxServerUrls(metaclass=Singleton):
    """
    Singleton class for dctx urls, to be imported by clients using those urls

    Attributes:
        dctx_server
        dctx_base_url
        dctx_one_state_base_url
        dctx_one_state_by_device_id_url
        dctx_all_states_by_username_url
        dctx_all_states_url
    """

    def __init__(self):
        self.__dctx_server = 'location'  # dctx, location, or policy
        self.__dctx_base_url = None
        self.__dctx_one_state_base_url = None
        self.__dctx_one_state_by_device_id_url = None
        self.__dctx_all_states_by_username_url = None
        self.__dctx_all_states_url = None
        self.set_dctx_urls()

    def set_dctx_urls(self):
        server_urls = ServerUrls.get_instance()
        if self.__dctx_server == 'dctx':
            dctx_server_port = 5005
        elif self.__dctx_server == 'location':
            dctx_server_port = ServerUrls.location_port
        else:
            assert False, "unsupported dctx server: {}".format(
                self.__dctx_server)

        location_host_url = server_urls.location_server_host_base_url
        dctx_server_host_base_url = location_host_url.replace(
            str(ServerUrls.location_port), str(dctx_server_port), 1)

        self.__dctx_states_base_url = (
            dctx_server_host_base_url + "magen/dctx/v1/states/")
        self.__dctx_one_state_base_url = self.__dctx_states_base_url + "state/"
        self.__dctx_one_state_by_device_id_url = self.__dctx_states_base_url + "device/{}/"
        self.__dctx_all_states_by_username_url = self.__dctx_states_base_url + "user/{}/"
        self.__dctx_all_states_url = self.__dctx_states_base_url

    @property
    def dctx_server(self):
        """
        process hosting dctx rest apis, used for building dctx rest api urls.
        One of location process, separate dctx process, or policy process.

        :return: 'location', 'dctx', 'policy'
        :rtype: string
        """
        return self.__dctx_server

    @property
    def dctx_one_state_base_url(self):
        """
        dctx rest api host,port,prefix, used for building dctx rest api urls.

        :return: http[s]://host[:port]/<prefix>
        :rtype: string
        """
        return self.__dctx_one_state_base_url

    @property
    def dctx_one_state_by_device_id_url(self):
        """
        dctx rest api url for getting one dctx_state record by device_id

        :return: url format string expecting a single device_id string argument
        :rtype: string
        """
        return self.__dctx_one_state_by_device_id_url

    @property
    def dctx_all_states_by_username_url(self):
        """
        dctx rest api url for getting all user's dctx_state records

        :return: url format string expecting a single user string argument
        :rtype: string
        """
        return self.__dctx_all_states_by_username_url

    @property
    def dctx_all_states_url(self):
        """
        dctx rest api url for getting all dctx_state records

        :return: url string (no format required)
        :rtype: string
        """
        return self.__dctx_all_states_url
