#! /usr/bin/python3
import sys
import json
from bson.json_util import loads, dumps
import unittest

from magen_dctx.dctx_lib.dctx_server_urls import DctxServerUrls

sys.path.append("..")

from policy.policy_server import policy_server

from policy.tests.policy_test_common import PolicyTestCommon
from policy.tests.policy_test_common_rest import *

from policy.tests.policy_test_misc_messages import *
from policy.tests.policy_test_contract_messages import *
from policy.tests.policy_test_template_messages import *
from policy.tests.policy_test_session_messages import *
from policy.tests.policy_test_validation_messages import *

from magen_location.tests.location_test_messages import *
from magen_dctx.tests.dctx_test_messages import *

__author__ = "Reinaldo Penno"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__license__ = "New-style BSD"
__version__ = "0.1"
__email__ = "rapenno@gmail.com"


class TestRestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        PolicyTestCommon.test_class_init(cls, __name__)

    def setUp(self):
        """
        This function prepares the system for running tests
        """
        PolicyTestCommon.delete_all_configuration(self)

    def tearDown(self):
        PolicyTestCommon.delete_all_configuration(self)
        PolicyTestCommon.check_no_policy(self)

    def test_ResetDemo(self):
        server_urls = ServerUrls.get_instance()
        RestClientApis.http_put_and_check_success(server_urls.policy_full_reset_url, None)
        PolicyTestCommon.check_no_policy(self)

    def test_FullReset(self):
        server_urls = ServerUrls.get_instance()
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_template_url,
                POLICY_TEMPLATE_POST_REQ_FINANCE,
                POLICY_TEMPLATE_GET_RESP_FINANCE).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_template_url,
                POLICY_TEMPLATE_POST_REQ_ACCOUNTING,
                POLICY_TEMPLATE_GET_RESP_ACCOUNTING).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_template_url,
                POLICY_TEMPLATE_POST_REQ_MARKETING,
                POLICY_TEMPLATE_GET_RESP_MARKETING).success, True)
        # Principal Group Policy contract
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_FINANCE_FROM_PT_FIRST_FLOOR,
                POLICY_CONTRACT_GET_RESP_FINANCE_FROM_PT_FIRST_FLOOR_NO_PI).success, True)
        # Principal contract
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_FINANCE_FROM_PT_BY_NUALA_FOR_ROD,
                POLICY_CONTRACT_GET_RESP_FINANCE_FROM_PT_BY_NUALA_FOR_ROD_NO_PI).success, True)
        # Principal contract
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_MARKETING_FROM_PT_BY_NUALA,
                POLICY_CONTRACT_GET_RESP_MARKETING_FROM_PT_BY_NUALA_NO_PI).success, True)
        RestClientApis.http_put_and_check_success(server_urls.policy_full_reset_url, None)
        PolicyTestCommon.check_no_policy(self)

    def test_Misc(self):
        server_urls = ServerUrls.get_instance()

        root_url = "http://" + server_urls.policy_server_url_host_port + "/"
        success, response = PolicyTestCommon.get_doc(root_url)
        self.assertIs(success, True)
        self.assertIs(response.status_code, HTTPStatus.OK.value)
        self.assertIs((response.text.find("Welcome to Policy") != -1), True)

        check_url = root_url + "check/"
        success, response = PolicyTestCommon.get_doc(check_url)
        self.assertIs(success, True)
        self.assertIs(response.status_code, HTTPStatus.OK.value)
        self.assertIs((response.text == "Check success"), True)

        html_url = root_url + "html/index.html"
        success, response = PolicyTestCommon.get_doc(html_url)
        self.assertIs(success, True)
        self.assertIs(response.status_code, HTTPStatus.OK.value)
        self.assertIs(
            (response.text.find(
                "ERROR: Documentation not currently built.") != -1) or
            (response.text.find(
                "Welcome to Magen Policy’s documentation!") != -1),
            True)

        log_url = server_urls.policy_server_base_url + "logging_level/"
        get_resp_object = RestClientApis.http_get_and_compare_resp(
            log_url,
            POLICY_MISC_GET_RESP_LOGGING_LEVEL_ERROR)
        self.assertIs(get_resp_object.success, True)

        message = POLICY_MISC_POST_LOGGING_LEVEL_INFO
        msg_dict = loads(message)
        rest_resp = RestClientApis.http_post_and_check_success(
            log_url, POLICY_MISC_POST_LOGGING_LEVEL_INFO)
        get_resp_object = RestClientApis.http_get_and_compare_resp(
            log_url, POLICY_MISC_GET_RESP_LOGGING_LEVEL_INFO)

        self.assertIs(
            RestClientApis.http_put_and_compare_get_resp(
                log_url,
                POLICY_MISC_POST_LOGGING_LEVEL_INFO,
                POLICY_MISC_GET_RESP_LOGGING_LEVEL_INFO).success, True)

    def test_DctxDB(self):
        # - add 3 state records, validating get by device_id
        # - update 1 state record
        # - delete state records by device_id and by all, verifying counts
        print("+++++++++Dctx Database Test+++++++++")
        server_urls = ServerUrls.get_instance()
        dctx_server_urls = DctxServerUrls()

        ptest_http_delete_many_and_verify(self, dctx_server_urls.dctx_all_states_url)

        message = DCTX_POST_REQ_COMPLIANT_IPAD
        dctx_dict = loads(message)
        ipad1_username = dctx_dict['magen_dctx_update']['device_states'][0]['username']
        ipad1_device_id = dctx_dict['magen_dctx_update']['device_states'][0]['device_id']
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                dctx_server_urls.dctx_one_state_base_url,
                dumps(dctx_dict),
                DCTX_GET_RESP_COMPLIANT_IPAD).success, True)
        message = DCTX_POST_REQ_NONCOMPLIANT_IPAD
        dctx_dict = loads(message)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                dctx_server_urls.dctx_one_state_base_url,
                dumps(dctx_dict),
                DCTX_GET_RESP_NONCOMPLIANT_IPAD).success, True)
        message = DCTX_POST_REQ_COMPLIANT_IPAD
        dctx_dict = loads(message)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                dctx_server_urls.dctx_one_state_base_url,
                dumps(dctx_dict),
                DCTX_GET_RESP_COMPLIANT_IPAD).success, True)

        message = DCTX_POST_REQ_COMPLIANT_MAC
        dctx_dict = loads(message)
        mac1_device_id = dctx_dict['magen_dctx_update']['device_states'][0]['device_id']
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                dctx_server_urls.dctx_one_state_base_url,
                dumps(dctx_dict),
                DCTX_GET_RESP_COMPLIANT_MAC).success, True)

        message = DCTX_POST_REQ_NONCOMPLIANT_MAC
        dctx_dict = loads(message)
        mac2_device_id = dctx_dict['magen_dctx_update']['device_states'][0]['device_id']
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                dctx_server_urls.dctx_one_state_base_url,
                dumps(dctx_dict),
                DCTX_GET_RESP_NONCOMPLIANT_MAC).success, True)

        get_resp_object = RestClientApis.http_get_and_compare_resp(
            dctx_server_urls.dctx_one_state_by_device_id_url.format(ipad1_device_id),
            DCTX_GET_RESP_COMPLIANT_IPAD)
        self.assertIs(get_resp_object.success, True)

        get_resp_object = RestClientApis.http_get_and_compare_resp(
            dctx_server_urls.dctx_all_states_by_username_url.format(ipad1_username),
            DCTX_GET_RESP_COMPLIANT_IPAD)
        self.assertIs(get_resp_object.success, True)

        get_resp_object = RestClientApis.http_get_and_check_success(
            dctx_server_urls.dctx_all_states_url)
        json_body = get_resp_object.json_body
        states = get_resp_object.json_body['response']['device_states']
        self.assertIs(len(states), 3)

        self.assertIs(RestClientApis.http_delete_and_get_check(
            dctx_server_urls.dctx_one_state_by_device_id_url.format(ipad1_device_id)).success, True)
        get_resp_object = RestClientApis.http_get_and_check_success(
            dctx_server_urls.dctx_all_states_url)
        states = get_resp_object.json_body['response']['device_states']
        self.assertIs(len(states), 2)

        self.assertIs(RestClientApis.http_delete_and_get_check(
            dctx_server_urls.dctx_one_state_by_device_id_url.format(mac1_device_id)).success, True)
        get_resp_object = RestClientApis.http_get_and_check_success(
            dctx_server_urls.dctx_all_states_url)
        states = get_resp_object.json_body['response']['device_states']
        self.assertIs(len(states), 1)

        ptest_http_delete_many_and_verify(self, dctx_server_urls.dctx_all_states_url) # 1 -> 0
        
    def test_DctxPosturePolicy(self):
        print("+++++++++ "
              "POST Contract with Principal =, "
              "PUT Users, PUT Single Client, Put Dctx Posture "
              "and "
              "Validate Test+++++++++")
        server_urls = ServerUrls.get_instance()
        dctx_server_urls = DctxServerUrls()
        
        ptest_http_delete_many_and_verify(self, dctx_server_urls.dctx_all_states_url)

        message = POLICY_CONTRACT_POST_REQ_FINANCE_DCTX_POSTURE
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                message,
                POLICY_CONTRACT_GET_RESP_FINANCE_DCTX_POSTURE_NO_PI).success,
            True)

        request_json = loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)
        resp_json = loads(POLICY_SESSION_GET_RESP_MAC_LIPMAN_ONE_PI)
        mc_id = PolicyTestCommon.create_and_check_policy_session(
            self, request_json,resp_json)

        assetId = 777 # good assetId, access will succeed
        assetName = "GoodAssetIdTestDoc"
        asset_access_url = make_validate_asset_access_url(mc_id, str(assetId), "open")
        self.assertIs(
            check_validation(
                asset_access_url,
                POLICY_VALIDATION_GET_RESP_DENIED_DCTX_POSTURE_NO_DCTX,
                "Checking Compliant Posture Validation Failure: No Dctx"),
            True)

        message = DCTX_POST_REQ_COMPLIANT_IPAD
        dctx_dict = loads(message)
        mac1_device_id = dctx_dict['magen_dctx_update']['device_states'][0]['device_id']
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                dctx_server_urls.dctx_one_state_base_url,
                dumps(dctx_dict),
                DCTX_GET_RESP_COMPLIANT_IPAD).success, True)

        assetId = 777 # good assetId, access will succeed
        assetName = "GoodAssetIdTestDoc"
        asset_access_url = make_validate_asset_access_url(mc_id, str(assetId), "open")
        self.assertIs(
            check_validation(
                asset_access_url,
                POLICY_VALIDATION_GET_RESP_GRANTED_GENERIC,
                "Checking Compliant Posture Validation Success"),
            True)

        message = DCTX_POST_REQ_NONCOMPLIANT_IPAD
        dctx_dict = loads(message)
        mac1_device_id = dctx_dict['magen_dctx_update']['device_states'][0]['device_id']
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                dctx_server_urls.dctx_one_state_base_url,
                dumps(dctx_dict),
                DCTX_GET_RESP_NONCOMPLIANT_IPAD).success, True)

        assetId = 777 # good assetId, noncompliant device
        assetName = "GoodAssetIdTestDoc"
        asset_access_url = make_validate_asset_access_url(mc_id, str(assetId), "open")
        self.assertIs(
            check_validation(
                asset_access_url,
                POLICY_VALIDATION_GET_RESP_DENIED_DCTX_POSTURE_NONCOMPLIANT,
                "Checking Compliant Posture Validation Falure: Non-compliant device"),
            True)

        ptest_http_delete_many_and_verify(self, dctx_server_urls.dctx_all_states_url)
        ptest_http_delete_many_and_verify(self, server_urls.policy_sessions_url)
        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)
        PolicyTestCommon.check_no_policy(self)

    def test_DctxSecurityGroupPolicy(self):
        print("+++++++++ "
              "POST Contract with Principal =, "
              "PUT Users, PUT Single Client, Put Dctx SecurityGroup"
              "and "
              "Validate Test+++++++++")
        server_urls = ServerUrls.get_instance()
        dctx_server_urls = DctxServerUrls()

        ptest_http_delete_many_and_verify(self,
                                          dctx_server_urls.dctx_all_states_url)

        message = POLICY_CONTRACT_POST_REQ_FINANCE_DCTX_SG_DEVOPS
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                message,
                POLICY_CONTRACT_GET_RESP_FINANCE_DCTX_SG_DEVOPS_NO_PI).success,
            True)

        request_json = loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)
        resp_json = loads(POLICY_SESSION_GET_RESP_MAC_LIPMAN_ONE_PI)
        mc_id = PolicyTestCommon.create_and_check_policy_session(
            self, request_json, resp_json)

        assetId = 777 # good assetId, access will succeed
        assetName = "GoodAssetIdTestDoc"
        asset_access_url = make_validate_asset_access_url(
            mc_id, str(assetId), "open")
        self.assertIs(
            check_validation(
                asset_access_url,
                POLICY_VALIDATION_GET_RESP_DENIED_DCTX_POSTURE_NO_DCTX,
                "Checking Compliant Posture Validation Failure: No Dctx"),
            True)

        message = DCTX_POST_REQ_SG_DEVOPS
        dctx_dict = loads(message)
        mac1_device_id = dctx_dict['magen_dctx_update']['device_states'][0]['device_id']
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                dctx_server_urls.dctx_one_state_base_url,
                dumps(dctx_dict),
                DCTX_GET_RESP_SG_DEVOPS).success, True)

        assetId = 777 # good assetId, access will succeed
        assetName = "GoodAssetIdTestDoc"
        asset_access_url = make_validate_asset_access_url(mc_id, str(assetId), "open")
        self.assertIs(
            check_validation(
                asset_access_url,
                POLICY_VALIDATION_GET_RESP_GRANTED_GENERIC,
                "Checking Security Group Validation Success"),
            True)

        message = DCTX_POST_REQ_COMPLIANT_IPAD
        dctx_dict = loads(message)
        mac1_device_id = dctx_dict['magen_dctx_update']['device_states'][0]['device_id']
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                dctx_server_urls.dctx_one_state_base_url,
                dumps(dctx_dict),
                DCTX_GET_RESP_COMPLIANT_IPAD).success, True)

        assetId = 777 # good assetId, noncompliant device
        assetName = "GoodAssetIdTestDoc"
        asset_access_url = make_validate_asset_access_url(mc_id, str(assetId), "open")
        self.assertIs(
            check_validation(
                asset_access_url,
                POLICY_VALIDATION_GET_RESP_DENIED_DCTX_SECURITY_GROUP_INVALID,
                "Checking Compliant Posture Validation Falure: Non-compliant device"),
            True)

        ptest_http_delete_many_and_verify(self, dctx_server_urls.dctx_all_states_url)
        ptest_http_delete_many_and_verify(self, server_urls.policy_sessions_url)
        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)
        PolicyTestCommon.check_no_policy(self)

    def test_RepoPolicy(self):
        print("+++++++++ "
              "POST Contract with Principal =, "
              "PUT Users, PUT Single Client, Put Dctx "
              "and "
              "Validate via SCM Test+++++++++")
        server_urls= ServerUrls.get_instance()
        dctx_server_urls = DctxServerUrls()
        application = "github"
        
        ptest_http_delete_many_and_verify(self, dctx_server_urls.dctx_all_states_url)

        message = POLICY_CONTRACT_POST_REQ_FINANCE_SCM_CLONE_DCTX_POSTURE
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                message,
                POLICY_CONTRACT_GET_RESP_FINANCE_SCM_CLONE_DCTX_POSTURE_NO_PI).success,
            True)

        request_json = loads(POLICY_SESSION_POST_REQ_LIPMAN_SCM_MAC)
        resp_json = loads(POLICY_SESSION_GET_RESP_MAC_LIPMAN_SCM_MAC_ONE_PI)
        mc_id = PolicyTestCommon.create_and_check_policy_session(
            self, request_json, resp_json)
        username = request_json['client']['user']

        repository = "repo_111"
        assetName = "GoodAssetIdTestDoc"
        repo_access_url = make_validate_repo_access_url(
            application, mc_id, username, str(repository), "clone")
        self.assertIs(
            check_validation(
                repo_access_url,
                POLICY_VALIDATION_GET_RESP_DENIED_DCTX_POSTURE_NO_DCTX,
                "Checking Compliant Posture Validation Failure: No Dctx"),
            True)

        message = DCTX_POST_REQ_COMPLIANT_IPAD
        dctx_dict = loads(message)
        mac1_device_id = dctx_dict['magen_dctx_update']['device_states'][0]['device_id']
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                dctx_server_urls.dctx_one_state_base_url,
                dumps(dctx_dict),
                DCTX_GET_RESP_COMPLIANT_IPAD).success, True)

        repository = "repo_111"
        assetName = "GoodAssetIdTestDoc"
        repo_access_url = make_validate_repo_access_url(
            application, mc_id, username, str(repository), "clone")
        self.assertIs(
            check_validation(
                repo_access_url,
                POLICY_VALIDATION_GET_RESP_GRANTED_KEYLESS,
                "Checking Compliant Posture Validation Success"),
            True)

        message = DCTX_POST_REQ_NONCOMPLIANT_IPAD
        dctx_dict = loads(message)
        mac1_device_id = dctx_dict['magen_dctx_update']['device_states'][0]['device_id']
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                dctx_server_urls.dctx_one_state_base_url,
                dumps(dctx_dict),
                DCTX_GET_RESP_NONCOMPLIANT_IPAD).success, True)

        repository = "repo_111"
        assetName = "GoodAssetIdTestDoc"
        repo_access_url = make_validate_repo_access_url(
            application, mc_id, username, str(repository), "clone")
        self.assertIs(
            check_validation(
                repo_access_url,
                POLICY_VALIDATION_GET_RESP_DENIED_DCTX_POSTURE_NONCOMPLIANT,
                "Checking Compliant Posture Validation Falure: Non-compliant device"),
            True)

        ptest_http_delete_many_and_verify(self, dctx_server_urls.dctx_all_states_url)
        ptest_http_delete_many_and_verify(self, server_urls.policy_sessions_url)
        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)
        PolicyTestCommon.check_no_policy(self)

    def test_PolicyTemplate(self):
        print("+++++++++Policy Template POST Test+++++++++")
        server_urls = ServerUrls.get_instance()
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_template_url,
                POLICY_TEMPLATE_POST_REQ_FINANCE,
                POLICY_TEMPLATE_GET_RESP_FINANCE).success, True)
        # Now we bring the system back to start and
        # check if everything was deleted
        ptest_http_delete_many_and_verify(self, server_urls.policy_templates_url)

    # This is the end-to-end test with exception of location
    def test_Sessions_PolicyTemplate_PolicyContract(self):
        print("+++++++++ Policy Template POST, Policy Contracts POST "
              "+++++++++")
        server_urls = ServerUrls.get_instance()
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_template_url,
                POLICY_TEMPLATE_POST_REQ_FINANCE,
                POLICY_TEMPLATE_GET_RESP_FINANCE).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_template_url,
                POLICY_TEMPLATE_POST_REQ_ACCOUNTING,
                POLICY_TEMPLATE_GET_RESP_ACCOUNTING).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_template_url,
                POLICY_TEMPLATE_POST_REQ_MARKETING,
                POLICY_TEMPLATE_GET_RESP_MARKETING).success, True)
        # Principal Group Policy contract
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_FINANCE_FROM_PT_FIRST_FLOOR,
                POLICY_CONTRACT_GET_RESP_FINANCE_FROM_PT_FIRST_FLOOR_NO_PI).success, True)
        # Principal contract
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_FINANCE_FROM_PT_BY_NUALA_FOR_ROD,
                POLICY_CONTRACT_GET_RESP_FINANCE_FROM_PT_BY_NUALA_FOR_ROD_NO_PI).success, True)
        # Principal contract
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_MARKETING_FROM_PT_BY_NUALA,
                POLICY_CONTRACT_GET_RESP_MARKETING_FROM_PT_BY_NUALA_NO_PI).success, True)

        PolicyTestCommon.create_and_check_multiple_policy_sessions(
            self,
            POLICY_SESSION_POST_REQS_BASELINE_CLIENTS,
            POLICY_SESSION_GET_RESPS_BASELINE_CLIENTS_NO_PI,
            getall_resp_str=POLICY_SESSION_GETALL_RESP_BASELINE_CLIENTS_NO_PI)

        # Now we bring the system back to start and
        # check if everything was deleted
        ptest_http_delete_many_and_verify(self, server_urls.policy_templates_url)

        # All the instances should have been deleted
        PolicyTestCommon.check_no_policy_instances_in_sessions(self)

        request_jsons = loads(POLICY_SESSION_POST_REQS_BASELINE_CLIENTS)['clients']
        for i in range(len(request_jsons)):
            mc_id = request_jsons[i]["client"]["mc_id"]
            url = server_urls.policy_single_session_url.format(mc_id)
            self.assertIs(RestClientApis.http_delete_and_get_check(url).success, True)
        PolicyTestCommon.check_no_policy(self)

    def test_PolicyTemplate_PolicyContract(self):
        print("+++++++++Policy Template POST, Policy Contract POST, "
              "Delete all Contracts and Templates Test+++++++++")
        server_urls = ServerUrls.get_instance()
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_template_url,
                POLICY_TEMPLATE_POST_REQ_FINANCE,
                POLICY_TEMPLATE_GET_RESP_FINANCE).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_FINANCE_FROM_PT_FIRST_FLOOR,
                POLICY_CONTRACT_GET_RESP_FINANCE_FROM_PT_FIRST_FLOOR_NO_PI).success, True)
        # Now we bring the system back to start and
        # check if everything was deleted
        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)

        # We check that all pc references were removed from template
        PolicyTestCommon.check_no_policy_contracts_in_templates(self)
        ptest_http_delete_many_and_verify(self, server_urls.policy_templates_url)

        PolicyTestCommon.check_no_policy(self)

        ptest_http_delete_many_and_verify(self, server_urls.policy_templates_url)

    def test_PolicyTemplate_PolicyContract_DeleteSingleContract(self):
        print("+++++++++Policy Template POST, Policy Contract POST, "
              "Delete all Contracts and Templates Test+++++++++")
        server_urls = ServerUrls.get_instance()
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_template_url,
                POLICY_TEMPLATE_POST_REQ_FINANCE,
                POLICY_TEMPLATE_GET_RESP_FINANCE).success, True)

        rest_return = RestClientApis.http_post_and_check_success(
            server_urls.policy_contract_url,
            POLICY_CONTRACT_POST_REQ_FINANCE_FROM_PT_FIRST_FLOOR)

        self.assertIs(rest_return.success, True)
        single_contract_url = rest_return.response_object.headers['location']
        self.assertIs(RestClientApis.http_get_and_compare_resp(
            single_contract_url,
            POLICY_CONTRACT_GET_RESP_FINANCE_FROM_PT_FIRST_FLOOR_NO_PI).success, True)
        ptest_http_delete_single_and_verify(self, single_contract_url)

        PolicyTestCommon.check_no_policy_contracts_in_templates(self)

        ptest_http_delete_many_and_verify(self, server_urls.policy_templates_url)
        PolicyTestCommon.check_no_policy(self)

    def test_SinglePolicyTemplate_SinglePolicyContract_DeleteSingleTemplate(self):
        print("+++++++++Policy Template POST, Policy Template Check, Policy Contract POST, "
              "Delete Single Template Test+++++++++")
        server_urls = ServerUrls.get_instance()
        rest_resp = RestClientApis.http_post_and_check_success(
            server_urls.policy_template_url,
            POLICY_TEMPLATE_POST_REQ_FINANCE)
        self.assertIs(rest_resp.success, True)
        single_template_url = rest_resp.response_object.headers['location']
        self.assertIs(RestClientApis.http_get_and_compare_resp(
            single_template_url,
            POLICY_TEMPLATE_GET_RESP_FINANCE).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_FINANCE_FROM_PT_FIRST_FLOOR,
                POLICY_CONTRACT_GET_RESP_FINANCE_FROM_PT_FIRST_FLOOR_NO_PI).success, True)

        ptest_http_delete_single_and_verify(self, single_template_url)

        # Everything should have been deleted
        PolicyTestCommon.check_no_policy(self)

    def test_PolicyContracts(self):
        print("+++++++++Policy Contracts POST Test+++++++++")
        server_urls = ServerUrls.get_instance()
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_MARKETING,
                POLICY_CONTRACT_GET_RESP_MARKETING).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_ENGINEERING_CAMPUS,
                POLICY_CONTRACT_GET_RESP_ENGINEERING_CAMPUS_NO_PI).success, True)
        # Now we bring the system back to start and
        # check if everything was deleted
        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)

        PolicyTestCommon.check_no_policy(self)

    def test_PolicyContract_WithCustomApps(self):
        print("+++++++++Policy Contracts POST with custom apps Test+++++++++")
        server_urls = ServerUrls.get_instance()
        # Creation should succeed because we remove empty location_name before
        # committing to DB
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_MARKETING_CUSTOM_APPS,
                POLICY_CONTRACT_GET_RESP_MARKETING_CUSTOM_APPS).success, True)
        # Now we bring the system back to start and
        # check if everything was deleted
        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)

        PolicyTestCommon.check_no_policy(self)

    def test_PolicyContract_WithBadLocation(self):
        print("+++++++++Policy Contracts POST with empty location_name Test+++++++++")
        server_urls = ServerUrls.get_instance()
        # Creation should succeed because we remove empty location_name before
        # committing to DB
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_MARKETING_EMPTY_LOCATION_NAME,
                POLICY_CONTRACT_GET_RESP_MARKETING_EMPTY_LOCATION_NAME).success, True)
        # Now we bring the system back to start and
        # check if everything was deleted
        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)

        PolicyTestCommon.check_no_policy(self)

    def test_PolicyContractsFailure_NoTemplate(self):
        server_urls = ServerUrls.get_instance()
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_MARKETING,
                POLICY_CONTRACT_GET_RESP_MARKETING).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_ENGINEERING_CAMPUS,
                POLICY_CONTRACT_GET_RESP_ENGINEERING_CAMPUS_NO_PI).success, True)
        # This test should fail because no templates exist
        self.assertIs(RestClientApis.http_post_and_check_success(
            server_urls.policy_contract_url,
            POLICY_CONTRACT_POST_REQ_FINANCE_FROM_PT_BY_NUALA_FOR_ROD).success, False)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_template_url,
                POLICY_TEMPLATE_POST_REQ_FINANCE,
                POLICY_TEMPLATE_GET_RESP_FINANCE).success, True)
        # We have put the template, we will try again.
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_FINANCE_FROM_PT_BY_NUALA_FOR_ROD,
                POLICY_CONTRACT_GET_RESP_FINANCE_FROM_PT_BY_NUALA_FOR_ROD_NO_PI).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_template_url,
                POLICY_TEMPLATE_POST_REQ_MARKETING,
                POLICY_TEMPLATE_GET_RESP_MARKETING).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_MARKETING_FROM_PT_BY_NUALA,
                POLICY_CONTRACT_GET_RESP_MARKETING_FROM_PT_BY_NUALA_NO_PI).success, True)
        self.assertIs(
            ptest_check(
                server_urls.policy_contracts_url + "?owner=nuala@cisco.com",
                POLICY_CONTRACT_GET_MANY_RESP_FROM_PT_BY_NUALA,
                "Querying for contracts and specific owner"), True)
        # Now we bring the system back to start and
        # check if everything was deleted
        ptest_http_delete_many_and_verify(self, server_urls.policy_templates_url)

        # PCs that are not child of templates should remain
        get_resp_obj = ptest_http_get(server_urls.policy_contracts_url)
        ptest_http_get_verify_success(self, get_resp_obj, "policy_contracts")

        # Now delete all contracts and check again
        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)

        ptest_http_delete_many_and_verify(self, server_urls.policy_templates_url)
        PolicyTestCommon.check_no_policy(self)

    def test_PolicyContracts_GetOwnerContracts(self):
        print("+++++++++Policy Contracts POST, Get Contracts for Owner Test+++++++++")
        server_urls = ServerUrls.get_instance()
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_template_url,
                POLICY_TEMPLATE_POST_REQ_FINANCE,
                POLICY_TEMPLATE_GET_RESP_FINANCE).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_template_url,
                POLICY_TEMPLATE_POST_REQ_MARKETING,
                POLICY_TEMPLATE_GET_RESP_MARKETING).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_MARKETING,
                POLICY_CONTRACT_GET_RESP_MARKETING).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_ENGINEERING_CAMPUS,
                POLICY_CONTRACT_GET_RESP_ENGINEERING_CAMPUS_NO_PI).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_FINANCE_FROM_PT_BY_NUALA_FOR_ROD,
                POLICY_CONTRACT_GET_RESP_FINANCE_FROM_PT_BY_NUALA_FOR_ROD_NO_PI).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_MARKETING_FROM_PT_BY_NUALA,
                POLICY_CONTRACT_GET_RESP_MARKETING_FROM_PT_BY_NUALA_NO_PI).success, True)
        self.assertIs(
            ptest_check(server_urls.policy_contracts_url + "?owner=nuala@cisco.com",
                        POLICY_CONTRACT_GET_MANY_RESP_FROM_PT_BY_NUALA,
                  "Querying for contracts and specific owner"), True)
        # Now we bring the system back to start and
        # check if everything was deleted
        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)
        ptest_http_delete_many_and_verify(self, server_urls.policy_templates_url)
        PolicyTestCommon.check_no_policy(self)

    # the policy contract will match multiple clients for the same user. This covers
    # the unique situation where a user have several devices on the network covered
    # by the same policy contract
    def test_MultipleClientsToUserPut_PostPolicycontract(self):
        print("+++++++++Multiple Clients to User PUT,"
              "POST Policy Contract Test+++++++++")
        server_urls = ServerUrls.get_instance()
        PolicyTestCommon.create_and_check_multiple_policy_sessions(
            self,
            POLICY_SESSION_POST_REQS_BASELINE_CLIENTS,
            POLICY_SESSION_GET_RESPS_BASELINE_CLIENTS_NO_PI)

        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_ENGINEERING_CAMPUS,
                POLICY_CONTRACT_GET_RESP_ENGINEERING_CAMPUS_MULTI_PI).success, True)

        # Now we bring the system back to start and
        # check if everything was deleted
        ptest_http_delete_many_and_verify(self, server_urls.policy_sessions_url)
        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)
        PolicyTestCommon.check_no_policy(self)

    def test_MultipleClientsPut(self):
        print("+++++++++Multiple Client PUT Test+++++++++")
        server_urls = ServerUrls.get_instance()
        PolicyTestCommon.create_and_check_multiple_policy_sessions(
            self,
            POLICY_SESSION_POST_REQS_BASELINE_CLIENTS,
            POLICY_SESSION_GET_RESPS_BASELINE_CLIENTS_NO_PI)

        # Now we bring the system back to start and
        # check if everything was deleted
        ptest_http_delete_many_and_verify(self, server_urls.policy_sessions_url)
        PolicyTestCommon.check_no_policy(self)

    def test_MultipleUsersPut_MultipleTemplates_GetTemplateForUser(self):
        print("+++++++++Multiple Users PUT, Multiple Templates POST, "
              "Get Templates for specific user Test+++++++++")
        server_urls = ServerUrls.get_instance()

        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_template_url,
                POLICY_TEMPLATE_POST_REQ_FINANCE,
                POLICY_TEMPLATE_GET_RESP_FINANCE).success, True)
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_template_url,
                POLICY_TEMPLATE_POST_REQ_ACCOUNTING,
                POLICY_TEMPLATE_GET_RESP_ACCOUNTING).success, True)
        self.assertIs(
            ptest_check(server_urls.policy_templates_url + "?user=nuala@cisco.com",
                        POLICY_TEMPLATE_GET_MANY_RESP_USER_FILTER,
                  "Querying for specific user"), True)
        # Now we bring the system back to start and
        # check if everything was deleted
        ptest_http_delete_many_and_verify(self, server_urls.policy_templates_url)
        PolicyTestCommon.check_no_policy(self)

    def test_PolicyContractPost_SingleClientPost(self):
        print("+++++++++Policy Contract POST, Single Client POST Test+++++++++")
        server_urls = ServerUrls.get_instance()
        rest_return = RestClientApis.http_post_and_check_success(
            server_urls.policy_contract_url,
            POLICY_CONTRACT_POST_REQ_FINANCE_FIRST_FLOOR)
        self.assertIs(rest_return.success, True)
        policy_contract_url = rest_return.response_object.headers['location']
        self.assertIs(RestClientApis.http_get_and_compare_resp(
            policy_contract_url,
            POLICY_CONTRACT_GET_RESP_FINANCE_FIRST_FLOOR_NO_PI).success, True)
        request_json = loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)
        resp_json = loads(POLICY_SESSION_GET_RESP_MAC_LIPMAN_ONE_PI)
        mc_id = PolicyTestCommon.create_and_check_policy_session(
            self, request_json, resp_json)
        url = server_urls.policy_single_session_url.format(mc_id)

        # Now we delete and check state of the system is back
        # to start. First delete the client
        self.assertIs(RestClientApis.http_delete_and_get_check(url).success, True)
        get_resp_obj = ptest_http_get(policy_contract_url)
        json_response = get_resp_obj.json_body["response"]
        policy_contract_dict = json_response["policy_contract"][0]
        pi_list = policy_contract_dict["PI_list"]
        self.assertIs(len(pi_list), 0)

        # No PI or PS should exist
        get_resp_obj = ptest_http_get(server_urls.policy_instances_url)
        ptest_http_get_verify_empty(self, get_resp_obj, "policy_instances")

        get_resp_obj = ptest_http_get(server_urls.policy_sessions_url)
        ptest_http_get_verify_empty(self, get_resp_obj, "policy_sessions")

        # Now delete policy contract
        ptest_http_delete_single_and_verify(self, policy_contract_url)
        PolicyTestCommon.check_no_policy(self)

    def test_SingleClientPost_PolicyContractPost(self):
        print("+++++++++Single Client POST, Policy Contract POST Test+++++++++")
        server_urls = ServerUrls.get_instance()
        request_json = loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)
        resp_json = loads(POLICY_SESSION_GET_RESP_MAC_LIPMAN_NO_PI)
        mc_id = PolicyTestCommon.create_and_check_policy_session(
            self, request_json, resp_json)
        session_url = server_urls.policy_single_session_url.format(mc_id)

        rest_return = RestClientApis.http_post_and_check_success(
            server_urls.policy_contract_url,
            POLICY_CONTRACT_POST_REQ_FINANCE_FIRST_FLOOR)
        self.assertIs(rest_return.success, True)
        policy_contract_url = rest_return.response_object.headers['location']
        self.assertIs(RestClientApis.http_get_and_compare_resp(
            policy_contract_url,
            POLICY_CONTRACT_GET_RESP_FINANCE_FIRST_FLOOR_ONE_PI).success, True)
        ptest_http_delete_single_and_verify(self, policy_contract_url)

        get_resp_obj = ptest_http_get(server_urls.policy_instances_url)
        ptest_http_get_verify_empty(self, get_resp_obj, "policy_instances")

        ptest_http_delete_single_and_verify(self, session_url)

        get_resp_obj = ptest_http_get(server_urls.policy_sessions_url)
        ptest_http_get_verify_empty(self, get_resp_obj, "policy_sessions")
        PolicyTestCommon.check_no_policy(self)

    def test_SingleClientPut_PolicyContractPost_DeleteAllContracts(self):
        print("+++++++++Single Client PUT, "
              "Policy Contract POST, "
              "Delete all contracts, "
              "Delete single client Test+++++++++")
        server_urls = ServerUrls.get_instance()
        request_json = loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)
        resp_json = loads(POLICY_SESSION_GET_RESP_MAC_LIPMAN_NO_PI)
        mc_id = PolicyTestCommon.create_and_check_policy_session(
            self, request_json, resp_json)
        session_url = server_urls.policy_single_session_url.format(mc_id)
        rest_resp = RestClientApis.http_post_and_check_success(
            server_urls.policy_contract_url, POLICY_CONTRACT_POST_REQ_FINANCE_FIRST_FLOOR)
        self.assertIs(rest_resp.success, True)
        policy_contract_url = rest_resp.response_object.headers['location']
        self.assertIs(RestClientApis.http_get_and_compare_resp(
            policy_contract_url,
            POLICY_CONTRACT_GET_RESP_FINANCE_FIRST_FLOOR_ONE_PI).success, True)
        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)

        get_resp_obj = ptest_http_get(server_urls.policy_instances_url)
        ptest_http_get_verify_empty(self, get_resp_obj, "policy_instances")

        # Policy Session should remain for now
        RestClientApis.http_get_and_check_success(session_url)

        ptest_http_delete_single_and_verify(self, session_url)

        # No Policy Sessions should remain
        get_resp_obj = ptest_http_get(server_urls.policy_sessions_url)
        ptest_http_get_verify_empty(self, get_resp_obj, "policy_sessions")
        PolicyTestCommon.check_no_policy(self)

    def test_SingleClientPost_PolicyContractPost_DeleteAllClients(self):
        print("+++++++++Single Client PUT, "
              "Policy Contract POST, "
              "Delete all clients, "
              "Delete single contract+++++++++")
        server_urls = ServerUrls.get_instance()
        request_json = loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)
        resp_json = loads(POLICY_SESSION_GET_RESP_MAC_LIPMAN_NO_PI)
        mc_id = PolicyTestCommon.create_and_check_policy_session(
            self, request_json, resp_json)
        url = server_urls.policy_single_session_url.format(mc_id)

        rest_resp = RestClientApis.http_post_and_check_success(
            server_urls.policy_contract_url,
            POLICY_CONTRACT_POST_REQ_FINANCE_FIRST_FLOOR)
        self.assertIs(rest_resp.success, True)
        policy_contract_url = rest_resp.response_object.headers['location']
        self.assertIs(RestClientApis.http_get_and_compare_resp(
            policy_contract_url,
            POLICY_CONTRACT_GET_RESP_FINANCE_FIRST_FLOOR_ONE_PI).success, True)

        ptest_http_delete_many_and_verify(self, server_urls.policy_sessions_url)

        # Need to check if PI reference was remove from contract

        get_resp_obj = ptest_http_get(policy_contract_url)
        json_response = get_resp_obj.json_body["response"]
        policy_contract_dict = json_response["policy_contract"][0]
        pi_list = policy_contract_dict["PI_list"]
        self.assertIs(len(pi_list), 0)

        get_resp_obj = ptest_http_get(server_urls.policy_instances_url)
        ptest_http_get_verify_empty(self, get_resp_obj, "policy_instances")

        ptest_http_delete_single_and_verify(self, policy_contract_url)
        PolicyTestCommon.check_no_policy(self)

    def test_PutUsers_PutClient_PostContract_GetEntitlements(self):
        print("+++++++++ PUT Users, PUT Single Client "
              "POST Contract with Principal = "" and "
              "GET Entitlements Test+++++++++")
        server_urls = ServerUrls.get_instance()
        request_json = loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)
        resp_json = loads(POLICY_SESSION_GET_RESP_MAC_LIPMAN_NO_PI)
        mc_id = PolicyTestCommon.create_and_check_policy_session(
            self, request_json, resp_json)
        url = server_urls.policy_single_session_url.format(mc_id)

        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_ENGINEERING_CAMPUS,
                POLICY_CONTRACT_GET_RESP_ENGINEERING_CAMPUS_ONE_PI).success, True)
        entitlements_uri = make_client_all_entitlements_url(mc_id)
        self.assertIs(
            check_validation(
                entitlements_uri,
                MAGEN_ENTITLEMENTS_GET_RESP_MAC_LIPMAN_SINGLE_SESSION_SINGLE_PI,
                "Checking Entitlements"),
            True)

        assetId = 1 # unused for entitlements check
        asset_access_url = make_validate_asset_access_url(None, str(assetId), "open")
        self.assertIs(
            check_validation(
                asset_access_url,
                POLICY_VALIDATION_GET_RESP_DENIED_MISSING_MIDTOKEN,
                "Checking Client Action Validation"),
            False) # no rest-ut fn yet to check json response on 4xx failure
        asset_access_url = make_validate_asset_access_url(123456789, None, "open")
        self.assertIs(
            check_validation(
                asset_access_url,
                POLICY_VALIDATION_GET_RESP_DENIED_MISSING_ASSETID,
                "Checking Client Action Validation"),
            False) # no rest-ut fn yet to check json response on 4xx failure
        asset_access_url = make_validate_asset_access_url(123456789, str(assetId), None)
        self.assertIs(
            check_validation(
                asset_access_url,
                POLICY_VALIDATION_GET_RESP_DENIED_MISSING_ACTION,
                "Checking Client Action Validation"),
            False) # no rest-ut fn yet to check json response on 4xx failure

        ptest_http_delete_many_and_verify(self, server_urls.policy_sessions_url)

        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)
        PolicyTestCommon.check_no_policy(self)

    def test_PutUsers_PutClient_PostContract_Validate(self):
        print("+++++++++ PUT Users, PUT Single Client "
              "POST Contract with Principal = "" and "
              "Validate Access Test+++++++++")
        server_urls = ServerUrls.get_instance()
        request_json = loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)
        resp_json = loads(POLICY_SESSION_GET_RESP_MAC_LIPMAN_NO_PI)
        mc_id = PolicyTestCommon.create_and_check_policy_session(
            self, request_json, resp_json)
        url = server_urls.policy_single_session_url.format(mc_id)

        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_ENGINEERING_CAMPUS,
                POLICY_CONTRACT_GET_RESP_ENGINEERING_CAMPUS_ONE_PI).success, True)
        entitlements_uri = make_client_all_entitlements_url(mc_id)

        # bad messages
        assetId = 1  # irrelevant for bad client_id test
        # bad client id
        asset_access_url = make_validate_asset_access_url(123456789, str(assetId), "open")
        self.assertIs(
            check_validation(
                asset_access_url,
                POLICY_VALIDATION_GET_RESP_DENIED_UNKNOWN_SESSION,
                "Checking Client Action Validation, Fail(1)"),
            True)

        assetId = 5555  # bad asset id
        assetName = "BadAssetIdTestDoc"
        asset_access_url = make_validate_asset_access_url(mc_id, str(assetId), "open")
        self.assertIs(
            check_validation(
                asset_access_url,
                POLICY_VALIDATION_GET_RESP_DENIED_INVALID_ASSETID,
                "Checking Client Action Validation, Fail(2)"),
            True)

        assetId = 777  # good assetId, fail on policy
        assetName = "GoodAssetIdTestDoc"
        asset_access_url = make_validate_asset_access_url(mc_id, str(assetId), "open")
        self.assertIs(
            check_validation(
                asset_access_url,
                POLICY_VALIDATION_GET_RESP_DENIED_LOCATION_MAC_LIPMAN_GET_SINGLE_SESSION_AND_SINGLE_CONTRACT,
                "Checking Client Action Validation, Fail(3)"),
            True)

        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)
        ptest_http_delete_many_and_verify(self, server_urls.policy_sessions_url)

        PolicyTestCommon.check_no_policy(self)

    def test_PostContract_PutUsers_PutClient_Validate(self):
        print("+++++++++ "
              "POST Contract with Principal =, "
              "PUT Users, PUT Single Client "
              " and "
              "Validate Test+++++++++")
        server_urls = ServerUrls.get_instance()
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_ENGINEERING_LOCATIONLESS,
                POLICY_CONTRACT_GET_RESP_ENGINEERING_LOCATIONLESS_NO_PI).success,
            True)
        request_json = loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)
        resp_json = loads(POLICY_SESSION_GET_RESP_MAC_LIPMAN_ONE_PI)
        mc_id = PolicyTestCommon.create_and_check_policy_session(
            self, request_json, resp_json)
        url = server_urls.policy_single_session_url.format(mc_id)

        assetId = 776 # error case: good assetId with no key
        assetName = "GoodAssetIdTestDoc"
        asset_access_url = make_validate_asset_access_url(mc_id, str(assetId), "open")
        self.assertIs(
            check_validation(
                asset_access_url,
                POLICY_VALIDATION_GET_RESP_DENIED_KEY_NOTFOUND_776,
                "Checking Client Action Locationless Validation"),
            True)

        assetId = 777 # good assetId, access will succeed
        assetName = "GoodAssetIdTestDoc"
        asset_access_url = make_validate_asset_access_url(mc_id, str(assetId), "open")
        self.assertIs(
            check_validation(
                asset_access_url,
                POLICY_VALIDATION_GET_RESP_GRANTED_GENERIC,
                "Checking Client Action Locationless Validation"),
            True)

        ptest_http_delete_many_and_verify(self, server_urls.policy_sessions_url)
        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)
        PolicyTestCommon.check_no_policy(self)

    def test_PutUsers_PutClient_LoadContracts_GetEntitlements(self):
        print("+++++++++ PUT Users, PUT Single Client "
              "POST Contract with Principal = "" and "
              "GET Entitlements Test+++++++++")
        server_urls = ServerUrls.get_instance()
        request_json = loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)
        resp_json = loads(POLICY_SESSION_GET_RESP_MAC_LIPMAN_NO_PI)

        mc_id = PolicyTestCommon.create_and_check_policy_session(
            self, request_json, resp_json)
        url = server_urls.policy_single_session_url.format(mc_id)
        self.assertIs(load_policies_test(), True)
        entitlements_uri = make_client_all_entitlements_url(mc_id)

        self.assertIs(
            check_validation(
                entitlements_uri,
                MAGEN_ENTITLEMENTS_GET_RESP_MAC_LIPMAN_SINGLE_SESSION_MULTI_PI,
                "Checking Entitlements"),
            True)

        ptest_http_delete_many_and_verify(self, server_urls.policy_sessions_url)
        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)
        PolicyTestCommon.check_no_policy(self)

    def test_GetEntitlements(self):
        print("+++++++++GET Entitlements Test+++++++++")
        server_urls = ServerUrls.get_instance()
        self.assertIs(load_policies_test(), True)
        request_json = loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)
        resp_json = loads(POLICY_SESSION_GET_RESP_MAC_LIPMAN_ONE_PI)
        mc_id = PolicyTestCommon.create_and_check_policy_session(
            self, request_json, resp_json)
        url = server_urls.policy_single_session_url.format(mc_id)

        entitlements_uri = make_client_all_entitlements_url(mc_id)
        self.assertIs(
            check_validation(
                entitlements_uri,
                MAGEN_ENTITLEMENTS_GET_RESP_MAC_LIPMAN_SINGLE_SESSION_MULTI_PI,
                "Checking Entitlements"),
            True)

        ptest_http_delete_many_and_verify(self,server_urls.policy_sessions_url)
        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)
        PolicyTestCommon.check_no_policy(self)

    def test_DeleteAllClients_Delete_allLocationTracking(self):
        print("+++++++++ Add Users, Add Clients, Add Policy with Location, "
              "Delete Clients, Check if all Location Stores were deleted+++++++++")
        server_urls = ServerUrls.get_instance()
        request_json = loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)
        resp_json = loads(POLICY_SESSION_GET_RESP_MAC_LIPMAN_NO_PI)
        mc_id = PolicyTestCommon.create_and_check_policy_session(
            self, request_json, resp_json)
        url = server_urls.policy_single_session_url.format(mc_id)
        # add a policy contract that has a location constraint
        rest_return_obj = RestClientApis.http_post_and_compare_get_resp(
            server_urls.policy_contract_url,
            POLICY_CONTRACT_POST_REQ_FINANCE_FIRST_FLOOR,
            POLICY_CONTRACT_GET_RESP_FINANCE_FIRST_FLOOR_ONE_PI)
        self.assertIs(rest_return_obj.success, True)

        success, entitlements = get_entitlements(mc_id)
        # print("entitlements: ===>", entitlements)

        # make sure we got back a single entitlement
        self.assertIs(len(entitlements['response']['r_groups']), 1)
        pi_uuid = entitlements['response']['r_groups'][
            0]['environment']['pdp-authorize']['cookie']
        # print(pi_uuid)

        # check location is invalid
        validation_uri = make_client_one_entitlement_url(mc_id, pi_uuid)

        print(validation_uri,
              POLICY_ENTITLEMENTS_GET_RESP_DENIED_LOCATION)

        self.assertIs(
            ptest_check(
                validation_uri,
                POLICY_ENTITLEMENTS_GET_RESP_DENIED_LOCATION,
                "check location denied"),
            True)

        # Deleting all clients need to delete all Location tracking
        ptest_http_delete_many_and_verify(self, server_urls.policy_sessions_url)
        get_resp_obj = ptest_http_get(server_urls.location_stores_url)
        ptest_http_get_verify_empty(self, get_resp_obj, "location_stores")

        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)
        PolicyTestCommon.check_no_policy(self)

    def test_location(self):
        """
        In this test client is insert first, therefore when policy contract is created it will
        have a valid policy instance list. Therefore the policy contract needs to be done against
        a different response from cases where the policy contract is created first.
        """
        print("+++++++++Update Location Test+++++++++")
        server_urls = ServerUrls.get_instance()
        single_client = loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)
        mc_id = single_client['client']['mc_id']

        request_json = single_client
        resp_json = loads(POLICY_SESSION_GET_RESP_MAC_LIPMAN_NO_PI)
        PolicyTestCommon.create_and_check_policy_session(self,request_json,resp_json)

        # add a policy contract that has a location constraint
        rest_resp = RestClientApis.http_post_and_check_success(
            server_urls.policy_contract_url,
            POLICY_CONTRACT_POST_REQ_FINANCE_FIRST_FLOOR)
        self.assertIs(rest_resp.success, True)
        policy_contract_url = rest_resp.response_object.headers['location']
        self.assertIs(RestClientApis.http_get_and_compare_resp(
            policy_contract_url,
            POLICY_CONTRACT_GET_RESP_FINANCE_FIRST_FLOOR_ONE_PI).success, True)

        success, entitlements = get_entitlements(mc_id)
        # print("entitlements: ===>", entitlements)

        # make sure we got back a single entitlement
        self.assertIs(len(entitlements['response']['r_groups']), 1)
        pi_uuid = entitlements['response']['r_groups'][
            0]['environment']['pdp-authorize']['cookie']
        # print(pi_uuid)

        # check location is invalid
        entitlement_uri = make_client_one_entitlement_url(mc_id, pi_uuid)

        self.assertIs(
            ptest_check(
                entitlement_uri,
                POLICY_ENTITLEMENTS_GET_RESP_DENIED_LOCATION,
                "check location denied"),
            True)

        # We put directly to Location Server in order to avoid deadlock
        location_server_update_url = server_urls.location_server_base_url + "lctx/notifications/locationupdate/"
        location_update_dict = json.loads(LOCATION_PUT_REQ_CAFETERIA)
        self.assertIs(
            RestClientApis.http_put_and_check_success(
                location_server_update_url,
                json.dumps(location_update_dict)).success, True)
        # check location is valid
        self.assertIs(
            ptest_check(
                entitlement_uri,
                POLICY_ENTITLEMENTS_GET_RESP_GRANTED_LOCATION,
                "check location ok"),
            True)

        # continue test as per CL Berlin
        success, policies = get_policy_contracts()
        self.assertIs(len(policies['response']['policy_contracts']), 1)
        pc_uuid = policies['response']['policy_contracts'][0]['uuid']

        # remove policy
        # Removing PC (and consequently PI) needs to remove location tracking
        resp_obj = PolicyTestCommon.delete_contract(pc_uuid)
        ptest_http_delete_verify_success(self, resp_obj)
        get_resp_obj = ptest_http_get(server_urls.policy_contracts_url)
        ptest_http_get_verify_empty(self, get_resp_obj, "policy_contracts")

        get_resp_obj = ptest_http_get(server_urls.policy_instances_url)
        ptest_http_get_verify_empty(self, get_resp_obj, "policy_instances")

        # add more restrictive policy
        self.assertIs(
            RestClientApis.http_post_and_compare_get_resp(
                server_urls.policy_contract_url,
                POLICY_CONTRACT_POST_REQ_FINANCE_CFO_OFFICE_LIPMAN,
                POLICY_CONTRACT_GET_RESP_FINANCE_CFO_OFFICE_LIPMAN_ONE_PI).success, True)

        success, entitlements = get_entitlements(mc_id)
        # print("entitlements: ===>", entitlements)

        # make sure we got back a single entitlement
        self.assertIs(len(entitlements['response']['r_groups']), 1)
        pi_uuid = entitlements['response']['r_groups'][
            0]['environment']['pdp-authorize']['cookie']
        # print(pi_uuid)

        # update validation uri with new PI uuid
        entitlement_uri = make_client_one_entitlement_url(mc_id, pi_uuid)

        # TODO:
        # update the new location validator with the current client location on contract addition -
        # right now this is a default location
        # either request an update from LCTX or store the location in the validator store
        #  with pi_uuid of 0 = client location
        # should request this from LCTX on behalf of all clients on server restart
        # After this works - add more test clauses below - remove cfo policy,
        # add it back, check location is still valid

        # check location no longer valid
        self.assertIs(
            ptest_check(
                entitlement_uri,
                POLICY_ENTITLEMENTS_GET_RESP_DENIED_LOCATION,
                "check location denied"),
            True)

        # We put directly to Location Server in order to avoid deadlock
        location_server_update_url = server_urls.location_server_base_url + "lctx/notifications/locationupdate/"
        location_update_dict = json.loads(LOCATION_PUT_REQ_CFO_OFFICE)
        self.assertIs(RestClientApis.http_put_and_check_success(
            location_server_update_url,
            json.dumps(location_update_dict)).success, True)

        # check location valid again
        self.assertIs(
            ptest_check(
                entitlement_uri,
                POLICY_ENTITLEMENTS_GET_RESP_GRANTED_LOCATION,
                "check location ok"),
            True)
        # All contracts is not removing all stores?
        ptest_http_delete_many_and_verify(self, server_urls.policy_contracts_url)

        get_resp_obj = ptest_http_get(server_urls.location_stores_url)
        ptest_http_get_verify_empty(self, get_resp_obj, "location_stores")

        session_url = server_urls.policy_single_session_url.format(mc_id)
        ptest_http_delete_single_and_verify(self, session_url)
        PolicyTestCommon.check_no_policy(self)

    def test_DeleteNonExistingContract(self):
        server_urls = ServerUrls.get_instance()
        single_contract_url = server_urls.policy_single_contract_url.format(
            "e5c9275c-271e-4fe4-82e9-0fe79a163f6d")
        resp_object = ptest_http_delete(single_contract_url)
        ptest_http_delete_verify_fail404(self, resp_object)
        PolicyTestCommon.check_no_policy(self)

    def test_PolicyMain_SetKeyServerUrlHostPort(self):
        policy_server.main(["--unittest", "--key-server-ip-port", "100.100.100.1:8000", "--mongo-ip-port", type(self).LOCAL_MONGO_LOCATOR])
        serverurls = ServerUrls().get_instance()
        self.assertEqual(serverurls.key_server_asset_url,
                         "http://100.100.100.1:8000/magen/ks/v3/asset_keys/assets/asset/")

    def test_PolicyMain_SetIngestionServerUrlHostPort(self):
        policy_server.main(["--unittest", "--ingestion-server-ip-port", "100.100.100.1:8000", "--mongo-ip-port", type(self).LOCAL_MONGO_LOCATOR])
        serverurls = ServerUrls().get_instance()
        self.assertEqual(serverurls.ingestion_server_asset_url,
                         "http://100.100.100.1:8000/magen/ingestion/v2/assets/asset/")

    def test_PolicyMain_SetIdentityServerUrlHostPort(self):
        policy_server.main(["--unittest", "--identity-server-ip-port", "100.100.100.1:8000", "--mongo-ip-port", type(self).LOCAL_MONGO_LOCATOR])
        serverurls = ServerUrls().get_instance()
        self.assertEqual(serverurls.identity_server_base_url,
                         "http://100.100.100.1:8000/magen/id/v2/")
