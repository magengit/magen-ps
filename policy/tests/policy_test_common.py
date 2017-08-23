import logging
from json import loads, dumps
import requests # for get_page()

from magen_logger.logger_config import LogDefaults, initialize_logger
from magen_utils_apis import domain_resolver
from magen_datastore_apis.main_db import MainDb
from magen_mongo_apis.mongo_core_database import MongoCore
from magen_mongo_apis.mongo_utils import MongoUtils
from magen_rest_apis.rest_client_apis import RestClientApis
from magen_rest_apis.server_urls import ServerUrls

from magen_dctx.dctx_lib.dctx_server_urls import DctxServerUrls

from policy.policy_server import policy_server

from policy.tests.policy_test_common_rest import ptest_http_get, \
    ptest_http_get_verify_empty, \
    ptest_http_get_verify_notfound, \
    ptest_http_delete, \
    ptest_http_delete_verify_success, \
    ptest_http_delete_many_and_verify, \
    ptest_http_get_verify_fail404

__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


class PolicyTestCommon(object):
    logger_init_cnt = 0
    
    @staticmethod
    def test_class_init(cls, tag):
        level="DEBUG"
        if PolicyTestCommon.logger_init_cnt == 0:
            logger = initialize_logger(
                console_level=level, output_dir="../logs/policy_pytest_logs")
            logger.setLevel(level)
        else:
            logger = logging.getLogger(LogDefaults.default_log_name)
        PolicyTestCommon.logger_init_cnt += 1
        logger.info("POLICY PYTEST %s LOGGING LEVEL: %s(%s) [init:%s]",
                    tag, level, logger.getEffectiveLevel(),
                    PolicyTestCommon.logger_init_cnt)

        cls.LOCAL_MONGO_LOCATOR = domain_resolver.mongo_locator()
        
        cls.db = MainDb.get_instance()
        cls.db.core_database = MongoCore.get_instance()
        cls.db.core_database.utils_strategy = MongoUtils.get_instance()
        cls.db.core_database.db_ip_port = cls.LOCAL_MONGO_LOCATOR
        cls.db.core_database.utils_strategy.check_db(cls.LOCAL_MONGO_LOCATOR)

        policy_server._ps_test_mode_url_locators_update_defaults()
        
    @staticmethod
    def get_doc(url):
        """
        RestClientApis assume response format that does not match
        doc urls (e.g. policy /check). Use this helper function instead.
        """
        s = requests.Session()
        try:
            get_response = s.get(url, timeout=2.0)
        except Exception as e:
            return False, e
        return True, get_response

    @staticmethod
    def check_no_policy_instances_in_sessions(test_instance):
        """
        Checks all PI references were removed from PS
        :param test_instance: instance of a test case
        :return: void
        """
        server_urls = ServerUrls.get_instance()
        get_resp_obj = ptest_http_get(server_urls.policy_sessions_url)
        json_response = get_resp_obj.json_body
        policy_session_list = json_response["response"]["policy_sessions"]
        for policy_session_dict in policy_session_list:
            policy_instance_list = policy_session_dict.get("policy_instances", [])
            test_instance.assertIs(len(policy_instance_list), 0)

    @staticmethod
    def check_no_policy_contracts_in_templates(test_instance):
        """
        Checks that all pc references were removed from template
        :param test_instance: instance of a test case
        :return: void
        """
        server_urls = ServerUrls.get_instance()
        get_resp_obj = ptest_http_get(server_urls.policy_templates_url)
        json_response = get_resp_obj.json_body
        policy_template_list = json_response["response"]["policy_templates"]
        for policy_template_dict in policy_template_list:
            policy_contract_list = policy_template_dict["policy_contracts"]
            test_instance.assertIs(len(policy_contract_list), 0)

    @staticmethod
    def check_no_policy(test_instance):
        """
        Checks that all pc references were removed from template
        :param test_instance: instance of a test case
        :return: void
        """
        server_urls = ServerUrls.get_instance()

        get_resp_obj = ptest_http_get(server_urls.policy_contracts_url)
        ptest_http_get_verify_notfound(
            test_instance, get_resp_obj, "policy_contracts",
            "No Policy Contracts found")

        get_resp_obj = ptest_http_get(server_urls.policy_instances_url)
        ptest_http_get_verify_empty(
            test_instance, get_resp_obj, "policy_instances")

        get_resp_obj = ptest_http_get(server_urls.policy_sessions_url)
        ptest_http_get_verify_empty(test_instance, get_resp_obj,
                                    "policy_sessions")

        get_resp_obj = ptest_http_get(server_urls.policy_templates_url)
        ptest_http_get_verify_notfound(
            test_instance, get_resp_obj, "policy_templates",
            "No Policy Templates found")

    @staticmethod
    def delete_all_configuration(test_instance):
        """
        Delete all configuration
        :param test_instance: instance of a test case
        :return: void
        """
        server_urls = ServerUrls.get_instance()
        dctx_server_urls = DctxServerUrls()
        del_resp_obj = ptest_http_delete(server_urls.policy_sessions_url)
        ptest_http_delete_verify_success(test_instance, del_resp_obj)
        del_resp_obj = ptest_http_delete(
            server_urls.policy_contracts_url)
        ptest_http_delete_verify_success(test_instance, del_resp_obj)
        del_resp_obj = ptest_http_delete(
            server_urls.policy_templates_url)
        ptest_http_delete_verify_success(test_instance, del_resp_obj)
        ptest_http_delete_many_and_verify(test_instance,
                                          dctx_server_urls.dctx_all_states_url)

    @staticmethod
    def delete_contract(uuid):
        """
        Delete a single contract
        :param uuid: UUID of magen_resource
        :return: True if successful, False otherwise
        """
        server_urls = ServerUrls.get_instance()
        single_contract_url = server_urls.policy_single_contract_url.format(uuid)
        return ptest_http_delete(single_contract_url)


    @staticmethod
    def create_and_check_policy_session(test_instance, request, response):
        """
        Given dict for json for a request to post to create a session and
        dict for json expected in response to a get on post's returned url,
        create the session and verify that the get response matches the
        expected response.

        return the mc_id for the request.
        """
        server_urls = ServerUrls.get_instance()
        test_instance.assertIs(RestClientApis.http_post_and_compare_get_resp(
            server_urls.policy_session_url,
            dumps(request), dumps(response)).success, True)
        mc_id = request["client"]['mc_id']
        return mc_id


    @staticmethod
    def create_and_check_multiple_policy_sessions(
            test_instance, requests_str, responses_str, *,
            getall_resp_str=None):
        server_urls = ServerUrls.get_instance()
        request_jsons = loads(requests_str)['clients']
        resp_jsons = loads(responses_str)["responses"]
        for i in range(len(request_jsons)):
            PolicyTestCommon.create_and_check_policy_session(
                test_instance, request_jsons[i], resp_jsons[i])
        if getall_resp_str != None:
            # Check to see that we can fetch all of the policy sessions at once
            test_instance.assertIs(
                RestClientApis.http_get_and_compare_resp(
                    server_urls.policy_sessions_url, getall_resp_str).success,
                True)
