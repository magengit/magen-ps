#! /usr/bin/python3
import logging

# Package imports from local PIP
from magen_logger.logger_config import LogDefaults
from magen_rest_apis.rest_client_apis import RestClientApis
from magen_rest_apis.server_urls import ServerUrls
from magen_utils_apis import compare_utils


from policy.tests.policy_test_contract_messages import POLICY_CONTRACT_PUT_REQ_BASELINE_CONTRACTS

__author__ = "repennor@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"

logger = logging.getLogger(LogDefaults.default_log_name)


def load_policies_test():
    print("\n Loading policies... \n")
    server_urls = ServerUrls.get_instance()
    url = server_urls.policy_contracts_url
    rest_resp = RestClientApis.http_put_and_check_success(url, POLICY_CONTRACT_PUT_REQ_BASELINE_CONTRACTS)
    if rest_resp.http_status != 200:
        print(
            "=>Failure to load policies. Response code = {} \n".format(
                rest_resp.http_status))
        return False

    elif not rest_resp.success:
        logger.error('Can not load policies.  %s', rest_resp.message)
        return False

    return True


def ptest_resp_cause_is_null(json_response):
    cause = json_response["response"]["cause"]
    return cause is None or cause == ""


def ptest_resp_result_is_null(json_response, result_key):
    val = json_response["response"][result_key]
    return val == "" or val == {} or val == []

            
# verify that expected success occurred and results are non-empty
def ptest_http_get(url):
    print("GET {} \n".format(url))
    return RestClientApis.http_get_and_check_success(url)


def ptest_http_get_verify_success_cmn(test_instance, resp_obj, result_key, expect_null):
    test_instance.assertTrue(resp_obj.success)
    json_response = resp_obj.json_body
    test_instance.assertEqual(json_response["status"], 200)
    if not expect_null:
        test_instance.assertTrue(ptest_resp_cause_is_null(json_response))
    test_instance.assertEqual(
        expect_null, ptest_resp_result_is_null(json_response, result_key))


def ptest_http_get_verify_success(test_instance, resp_obj, result_key):
    ptest_http_get_verify_success_cmn(test_instance, resp_obj, result_key, False)


def ptest_http_get_verify_empty(test_instance, resp_obj, result_key):
    ptest_http_get_verify_success_cmn(test_instance, resp_obj, result_key, True)


# verify that expected failure (status 404) occurred
def ptest_http_get_verify_fail404(test_instance, resp_obj, cause=None):
    test_instance.assertFalse(resp_obj.success)
    json_response = resp_obj.json_body
    test_instance.assertEqual(json_response["status"], 404)
    if cause:
        test_instance.assertEqual(json_response["response"]["cause"], cause)


# verify that expected failure occurred
# some calls in the unit test fail with 404 or 200 in different conditions
# so allow both for those cases
def ptest_http_get_verify_notfound(test_instance, resp_obj, key, cause):
    if not resp_obj.success:
        ptest_http_get_verify_fail404(test_instance, resp_obj, cause)
    else:
        ptest_http_get_verify_empty(test_instance, resp_obj, key)


def get_json(url):
    print("GET {} \n".format(url))
    get_resp_obj = RestClientApis.http_get_and_check_success(url)
    json_response = get_resp_obj.json_body
    status_code = json_response["status"]
    if status_code == 200:
        print("=>Check successful \n")
        return True, json_response
    else:
        print("=>Check not successful, error code: {}. \n".format(status_code))
        return False, json_response


def ptest_http_delete(url):
    print("DELETE {} \n".format(url))
    return RestClientApis.http_delete_and_check_success(url)


def ptest_http_delete_verify_success(test_instance, resp_obj):
    test_instance.assertTrue(resp_obj.success)
    json_response = resp_obj.json_body
    test_instance.assertEqual(json_response["status"], 200)


# verify that expected failure (status 404) occurred
def ptest_http_delete_verify_fail404(test_instance, resp_obj):
    test_instance.assertFalse(resp_obj.success)
    json_response = resp_obj.json_body
    test_instance.assertEqual(json_response["status"], 404)

def _ptest_delete_cmn_and_verify(test_instance, url):
    del_resp_obj = ptest_http_delete(url)
    del_json_response = del_resp_obj.json_body
    del_status = del_json_response["status"]
    if not del_resp_obj.success or del_status != 200:
        print("=>Delete not successful, error code: {} \n".format(del_status))
        test_instance.assertTrue(False)
    get_resp_obj = ptest_http_get(url)
    return get_resp_obj

def ptest_http_delete_many_and_verify(test_instance, url):
    get_resp_obj = _ptest_delete_cmn_and_verify(test_instance, url)
    get_json_response = get_resp_obj.json_body
    get_status = get_json_response["status"]
    if not get_resp_obj.success or get_status != 200:
        print("=>Delete many check: success:{}, error code:{}. \n".format(
            get_resp_obj.success, get_status))
        test_instance.assertTrue(False)
        
    print("=>Delete check successful \n")

def ptest_http_delete_single_and_verify(test_instance, url):
    get_resp_obj = _ptest_delete_cmn_and_verify(test_instance, url)
    get_json_response = get_resp_obj.json_body
    get_status = get_json_response["status"]
    if get_resp_obj.success or get_status != 404:
        print("=>Delete single check: success:{}, error code:{}. \n".format(
            get_resp_obj.success, get_status))
        test_instance.assertTrue(False)
        
    print("=>Delete check successful \n")

def ptest_check(url, json_resp, message, dd_mock=None):
    """
    Given a URL it performs a GET and checks if response matches expected response
    :param url: URL of GET request
    :param json_resp: expected JSON response
    :param message: message to print
    :param dd_mock: mock for events calls
    :return: True if checks, otherwise False
    """
    if dd_mock:
        dd_mock.start()
    print(message, "\n")

    rest_resp = RestClientApis.http_get_and_compare_resp(
        url,
        json_resp,
        compare_utils.full_compare_except_keys(['PI_list', 'policy_template_uuid', 'pi_uuid'])
    )
    if dd_mock:
        dd_mock.stop()
    if not rest_resp.success:
        print(json_resp)
    return rest_resp.success

# FIXME: when we handle resource group of one for documents - need to make sure that the UUID for the documents
# in the unit test are unique and don't change - should add files to the
# repository with the unique UUID


def make_validate_asset_access_url(client_uuid, assetId, action):
    server_urls = ServerUrls.get_instance()
    asset_access_url = server_urls.policy_validate_asset_access_url.format(
        (assetId))
    asset_access_url += "?application=box"
    if client_uuid:
        asset_access_url += "&midToken=" + str(client_uuid)
    if action:
        asset_access_url += "&action=" + action
    asset_access_url += "&returnKey=True"
    return asset_access_url


def make_validate_repo_access_url(application, client_id, username, repository,
                                  action):
    server_urls = ServerUrls.get_instance()
    repo_access_url = (server_urls.policy_validation_base_url +
                      "repository/{}/").format((repository))
    print("URL", repo_access_url)
    if application:
        repo_access_url += "?application=" + application
    if client_id:
        repo_access_url += "&client_id=" + client_id
    if username:
        repo_access_url += "&username=" + username
    if action:
        repo_access_url += "&action=" + action
    return repo_access_url


def make_client_all_entitlements_url(client_uuid):
    server_urls = ServerUrls.get_instance()
    entitlements_url = (server_urls.policy_server_base_url + "entitlements/" +
                        "?midToken=" + str(client_uuid))
    return entitlements_url

def make_client_one_entitlement_url(mc_id, pi_uuid):
    server_urls = ServerUrls.get_instance()
    entitlements_url = (server_urls.policy_server_base_url +
                        "entitlements/entitlement/" +
                        "?midToken=" + str(mc_id) +
                        "&pi_uuid=" + str(pi_uuid))
    return entitlements_url


def get_entitlements(uuid):
    """
    Return entitlements for a client
    :param uuid:  UUID of magen_resource
    :return: JSON string containing entitlements or None
    """
    server_urls = ServerUrls.get_instance()
    url = (server_urls.policy_server_base_url + "entitlements/" +
           "?midToken=" + str(uuid))
    return get_json(url)


def check_validation(url, json_resp, message, event_mock=None):
    if event_mock:
        event_mock.start()
    print(message, "\n")
    rest_resp = RestClientApis.http_get_and_compare_resp(url, json_resp, compare_utils.full_compare_except_keys(['pi_uuid', 'mc_id', 'cookie', 'resource_id']))
    if event_mock:
        event_mock.stop()
    if rest_resp.success:
        return True
    else:
        print("check_validation failed: {}".format(rest_resp.message))
        return False


def get_policy_contracts():
    """
    Return all policy contracts
    :return: JSON string containing all contracts or None
    """
    server_urls = ServerUrls.get_instance()
    url = server_urls.policy_contracts_url
    return get_json(url)
