#! /usr/bin/python3

import json
import unittest
from http import HTTPStatus
from unittest.mock import patch

from flask import Flask

from magen_rest_apis.rest_client_apis import RestClientApis
from magen_rest_apis.rest_return_api import RestReturn
from magen_rest_apis.server_urls import ServerUrls

from policy.policy_libs.policy_eventing import DDPolicyEventsWrapper
from policy.policy_libs.plib_ingestsvc import PlibIngestSvc
from policy.policy_libs.plib_keysvc import PlibKeySvc
from policy.policy_libs.policy_state import PolicyState
from policy.policy_server.policy_contract_rest_api import policy_contract_v2
from policy.policy_server.policy_session_rest_api import policy_session_v2
from policy.policy_server.policy_validation_rest_api import policy_validation_v2
from policy.tests.policy_test_common_rest import make_validate_asset_access_url

from policy.tests.policy_test_common import PolicyTestCommon
from policy.tests.services_mock_messages import \
    INGESTION_ASSET_GET_RESP_FOUND, INGESTION_ASSET_GET_RESP_NOTFOUND, \
    KEYSVC_ASSET_GET_RESP_NOTFOUND
from policy.tests.policy_test_contract_messages import \
    POLICY_CONTRACT_POST_REQ_ENGINEERING_LOCATIONLESS
from policy.tests.policy_test_session_messages import \
    POLICY_SESSION_POST_REQ_MAC_LIPMAN
from policy.tests.policy_test_validation_messages import \
    POLICY_VALIDATION_GET_RESP_GRANTED_GENERIC, \
    POLICY_VALIDATION_GET_RESP_DENIED_KEY_NOTFOUND_TA, \
    POLICY_VALIDATION_GET_RESP_DENIED_INVALID_ASSETID, \
    POLICY_VALIDATION_GET_RESP_DENIED_UNKNOWN_SESSION

__author__ = "Alena Lifar"
__email__ = "alifar@cisco.com"
__version__ = "0.1"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__status__ = "alpha"

DOCKER_MONGO_HOST = "magen_mongo"

TEST_ASSET_ID = "test_asset"

# Ideally all events check would be done as part of policy_basic_test.py
# - policy_basic_test.py runs policy server in a separate process (also
#   runs location server in a different process)
# - this behavior doesn't allow to use unittest.mock and unittest.mock.patch,
#   thus does not provide a way for unit test to verify the generated event.
# So, for now, run event tests separately, in the same process as pytest.
# Issues until all of policy runs in same process as pytest:
# - duplication of tests
# - modes inside software under test get more complicated, since, during
#   event tests, policy server thinks it is running in production mode.
# - these event tests are not included in coverage (which is only on/in
#   policy server process)


def assert_event(client_uuid, validation_dict, event_mock, policy_name, alert):
    """
    Event send_event called with parameters
    :param client_uuid:
    :param validation_dict: dictionary that was returned by PDP
    :param event_mock: MagicMock object
    :param policy_name: string
    :param alert: string = 'warning', 'success', 'error'
    :return: void
    """
    kwgs = dict(
        action=EventsTest.action_open,
        application=EventsTest.box_app,
        resource_id=TEST_ASSET_ID,
        client_id=client_uuid,
        policy=policy_name
    )
    event_data = DDPolicyEventsWrapper.construct_event(validation_dict, **kwgs)
    # Check that event was proper created and send method was called with correct parameters
    event_mock.assert_called_once_with(
        event_name=EventsTest.policy_event_title, event_data=event_data, alert=alert
    )


# in test mode, use mid_token itself as mc_id
def plib_id_auth_clt_mcid_from_midtoken_mock(self, mid_token):
    print("======== Mocking id service mcid from midtoken ========")
    return mid_token


class EventsTest(unittest.TestCase):
    db = None
    action_open = 'file.open'
    action_create = 'file.create'
    action_share = 'collaborator.added'
    box_app = 'box'
    test_policy = 'eng policy'
    unknown_policy = 'Unknown'
    policy_event_title = 'Policy Validation'

    @classmethod
    def setUpClass(cls):
        PolicyTestCommon.test_class_init(cls, __name__)

    def setUp(self):
        magen = Flask(__name__)
        magen.config['TESTING'] = True
        pfx = PolicyState().policy_v2_url_pfx
        magen.register_blueprint(policy_contract_v2,
                                 url_prefix=pfx + '/contracts')
        magen.register_blueprint(policy_session_v2,
                                 url_prefix=pfx + '/sessions')
        magen.register_blueprint(policy_validation_v2,
                                 url_prefix=pfx + '/validation')
        self.app = magen.test_client()
        self.rest_client_get_calls_count = 0
        self.server_urls = ServerUrls.get_instance()

    def tearDown(self):
        """
        Drop Collections
        :return: void
        """
        EventsTest.db.core_database.magen_mdb.drop_collection('policy_contracts')
        EventsTest.db.core_database.magen_mdb.drop_collection('policy_sessions')
        EventsTest.db.core_database.magen_mdb.drop_collection('policy_instances')
        EventsTest.db.core_database.magen_mdb.drop_collection('resource_documents')
        EventsTest.db.core_database.magen_mdb.drop_collection('assets')

    def add_policy_contract(self, pc_data):
        """
        Adding pc_data to DB using flask test_client
        :param pc_data: json str
        :return:void
        """
        # Adding Policy Contract
        policy_contract_create_resp = self.app.post(
            self.server_urls.policy_contract_url,
            data=pc_data,
            headers=RestClientApis.put_json_headers
        )
        self.assertEquals(policy_contract_create_resp.status_code, HTTPStatus.CREATED)

    def add_policy_session(self, ps_data):
        """
        Adding ps_data to DB using flask test_client
        :param ps_data: json str
        :return: void
        """
        # Adding Policy Session or a `Client`
        policy_session_create_resp = self.app.post(
            self.server_urls.policy_session_url,
            data=ps_data,
            headers=RestClientApis.put_json_headers
        )
        self.assertEquals(policy_session_create_resp.status_code, HTTPStatus.CREATED)

    def assert_validation(self, validation_resp_obj, test_data, status):
        """
        Helper method to make certain assertions after making validation call to Policy
        deciding it and return dictionary
        :param validation_resp_obj: response object from policy
        :param test_data: test string to assert against it
        :param status: HTTPStatus enum object
        :return: dict from validation_resp_obj
        """
        # Validating Successful
        self.assertEquals(validation_resp_obj.status_code, status)
        # decoding bytes to str
        validation_get_resp_dict = json.loads(validation_resp_obj.data.decode("utf-8"))
        self.assertDictEqual(validation_get_resp_dict, json.loads(test_data))
        print(validation_get_resp_dict)
        return validation_get_resp_dict

    # TESTS

    def test_EventValidationSuccess(self):
        """
        Post Policy Contract
        Post Policy Session
        Mock successful calls to KEY and INGESTION
        Validation check
        Event Assertion of created event
        :return: void
        """
        print()
        print("======= Test Event Validation Success =======")
        self.add_policy_contract(POLICY_CONTRACT_POST_REQ_ENGINEERING_LOCATIONLESS)
        self.add_policy_session(POLICY_SESSION_POST_REQ_MAC_LIPMAN)

        # Load string to retrieve mc_id
        mlipman_client_dict = json.loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)

        # Mock Rest Client Get Call with different parameters
        def rest_client_get_mock_success(url):
            print("======== Mocking RestClient Get calls ========")
            p_ingest_svc = PlibIngestSvc()
            p_key_svc = PlibKeySvc()
            if p_ingest_svc.single_asset_url(TEST_ASSET_ID) == url:
                # Successful ingestion check for test asset
                return RestReturn(
                    success=True,
                    http_status=HTTPStatus.OK,
                    message=HTTPStatus.OK.phrase,
                    json_body=json.loads(INGESTION_ASSET_GET_RESP_FOUND),
                    response_object=None
                )
            elif p_key_svc.single_asset_url(TEST_ASSET_ID) == url:
                # Successful key check for test asset
                return RestReturn(
                    success=True,
                    http_status=HTTPStatus.OK,
                    message=HTTPStatus.OK.phrase,
                    json_body=json.loads(POLICY_VALIDATION_GET_RESP_GRANTED_GENERIC),
                    response_object=None
                )

        # Get Validation Url for a test action
        validation_url = make_validate_asset_access_url(
            client_uuid=mlipman_client_dict["client"]["mc_id"],
            assetId=TEST_ASSET_ID,
            action=EventsTest.action_open
        )

        # Invoking validation call where Event to datadog is created and sent
        # mocking RestClientApis call from PolicyValidationApi._insvc_asset_metadata_get_by_assetId
        # mocking RestClientApis call from PolicyValidationApi._keysvc_asset_key_get_by_assetId
        with patch('magen_rest_apis.rest_client_apis.RestClientApis.http_get_and_check_success',
                   new=rest_client_get_mock_success), \
                patch('policy.policy_server.policy_validation_rest_api.PlibIdSvc.auth_clt_mcid_from_midtoken',
                      new=plib_id_auth_clt_mcid_from_midtoken_mock):
            with patch('policy.policy_libs.policy_eventing.DDPolicyEventsWrapper.send_event') as event_mock:

                validation_get_resp_obj = self.app.get(
                    validation_url,
                    headers=RestClientApis.get_json_headers
                )

                # Policy Validation Assert
                validation_get_resp_dict = self.assert_validation(
                    validation_get_resp_obj,
                    POLICY_VALIDATION_GET_RESP_GRANTED_GENERIC,
                    HTTPStatus.OK
                )

                # Event Call Assert
                assert_event(
                    mlipman_client_dict["client"]["mc_id"],
                    validation_get_resp_dict['response'],
                    event_mock,
                    EventsTest.test_policy,
                    alert='success'
                )

    def test_EventValidationFailKeyNotFound(self):
        """
        Post Policy Contract
        Post Policy Session
        Mock successful call to INGESTION on GET asset
        Mock key_not_found call to KEY on GET key for asset
        Validation check
        Event Assertion of created event
        :return: void
        """
        self.add_policy_contract(POLICY_CONTRACT_POST_REQ_ENGINEERING_LOCATIONLESS)
        self.add_policy_session(POLICY_SESSION_POST_REQ_MAC_LIPMAN)

        # Load string to retrieve mc_id
        mlipman_client_dict = json.loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)

        # Mock Rest Client Get Call with different parameters
        def rest_client_get_mock_fail_key_not_found(url):
            print("======== Mocking RestClient Get calls ========")
            p_ingest_svc = PlibIngestSvc()
            p_key_svc = PlibKeySvc()
            if p_ingest_svc.single_asset_url(TEST_ASSET_ID) == url:
                # Successful ingestion check for test asset
                return RestReturn(
                    success=True,
                    http_status=HTTPStatus.OK,
                    message=HTTPStatus.OK.phrase,
                    json_body=json.loads(INGESTION_ASSET_GET_RESP_FOUND),
                    response_object=None
                )
            elif p_key_svc.single_asset_url(TEST_ASSET_ID) == url:
                # Key Not Found check for test asset
                return RestReturn(
                    success=True,
                    http_status=HTTPStatus.OK,
                    message=HTTPStatus.OK.phrase,
                    json_body=json.loads(KEYSVC_ASSET_GET_RESP_NOTFOUND),
                    response_object=None
                )

        # Get Validation Url for a test action
        validation_url = make_validate_asset_access_url(
            client_uuid=mlipman_client_dict["client"]["mc_id"],
            assetId=TEST_ASSET_ID,
            action=EventsTest.action_open
        )

        # Invoking validation call where Event to datadog is created and sent
        # mocking RestClientApis call from PolicyValidationApi._isvc_asset_metadata_get_by_assetId
        # mocking RestClientApis call from PolicyValidationApi._keysvc_asset_key_get_by_assetId
        with patch('magen_rest_apis.rest_client_apis.RestClientApis.http_get_and_check_success',
                   new=rest_client_get_mock_fail_key_not_found), \
                patch('policy.policy_server.policy_validation_rest_api.PlibIdSvc.auth_clt_mcid_from_midtoken',
                      new=plib_id_auth_clt_mcid_from_midtoken_mock):
            with patch('policy.policy_libs.policy_eventing.DDPolicyEventsWrapper.send_event') as event_mock:
                validation_get_resp_obj = self.app.get(
                    validation_url,
                    headers=RestClientApis.get_json_headers
                )

                # Policy Validation Assert
                validation_get_resp_dict = self.assert_validation(
                    validation_get_resp_obj,
                    POLICY_VALIDATION_GET_RESP_DENIED_KEY_NOTFOUND_TA,
                    status=HTTPStatus.OK
                )

                # Event Call Assert
                assert_event(
                    mlipman_client_dict["client"]["mc_id"],
                    validation_get_resp_dict['response'],
                    event_mock,
                    EventsTest.test_policy,
                    alert='warning'
                )

    def test_EventValidationFailAssetNotFound(self):
        """
        Post Policy Contract
        Post Policy Session
        Mock asset_not_found call to INGESTION on GET asset
        Validation check
        Event Assertion of created event
        :return: void
        """
        self.add_policy_contract(POLICY_CONTRACT_POST_REQ_ENGINEERING_LOCATIONLESS)
        self.add_policy_session(POLICY_SESSION_POST_REQ_MAC_LIPMAN)

        # Load string to retrieve mc_id
        mlipman_client_dict = json.loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)

        # Mock Rest Client Get Call with different parameters
        def rest_client_get_mock_fail_asset_not_found(url):
            print("======== Mocking RestClient Get calls ========")
            p_ingest_svc = PlibIngestSvc()
            if p_ingest_svc.single_asset_url(TEST_ASSET_ID) == url:
                # Successful ingestion check for test asset
                return RestReturn(
                    success=True,
                    http_status=HTTPStatus.NOT_FOUND,
                    message=HTTPStatus.NOT_FOUND.phrase,
                    json_body=json.loads(INGESTION_ASSET_GET_RESP_NOTFOUND),
                    response_object=None
                )

        # Get Validation Url for a test action
        validation_url = make_validate_asset_access_url(
            client_uuid=mlipman_client_dict["client"]["mc_id"],
            assetId=TEST_ASSET_ID,
            action=EventsTest.action_open
        )

        # Invoking validation call where Event to datadog is created and sent
        # mocking RestClientApis call from PolicyValidationApi._isvc_asset_metadata_get_by_assetId
        with patch('magen_rest_apis.rest_client_apis.RestClientApis.http_get_and_check_success',
                   new=rest_client_get_mock_fail_asset_not_found), \
                patch('policy.policy_server.policy_validation_rest_api.PlibIdSvc.auth_clt_mcid_from_midtoken',
                      new=plib_id_auth_clt_mcid_from_midtoken_mock):
            with patch('policy.policy_libs.policy_eventing.DDPolicyEventsWrapper.send_event') as event_mock:
                validation_get_resp_obj = self.app.get(
                    validation_url,
                    headers=RestClientApis.get_json_headers
                )

                # Policy Validation Assert
                validation_get_resp_dict = self.assert_validation(
                    validation_get_resp_obj,
                    POLICY_VALIDATION_GET_RESP_DENIED_INVALID_ASSETID,
                    status=HTTPStatus.OK
                )

                # Event Call Assert
                assert_event(
                    mlipman_client_dict["client"]["mc_id"],
                    validation_get_resp_dict['response'],
                    event_mock,
                    EventsTest.unknown_policy,
                    alert='warning'
                )

    def test_EventValidationFailClientNotFound(self):
        """
        Post Policy Contract
        Validation check
        Event Assertion of created event
        :return: void
        """
        self.add_policy_contract(POLICY_CONTRACT_POST_REQ_ENGINEERING_LOCATIONLESS)

        # Load string to retrieve mc_id
        mlipman_client_dict = json.loads(POLICY_SESSION_POST_REQ_MAC_LIPMAN)

        # Get Validation Url for a test action
        validation_url = make_validate_asset_access_url(
            client_uuid=mlipman_client_dict["client"]["mc_id"],
            assetId=TEST_ASSET_ID,
            action=EventsTest.action_open
        )

        with patch('policy.policy_server.policy_validation_rest_api.PlibIdSvc.auth_clt_mcid_from_midtoken',
                   new=plib_id_auth_clt_mcid_from_midtoken_mock):
            # Invoking validation call where Event to datadog is created and sent
            with patch('policy.policy_libs.policy_eventing.DDPolicyEventsWrapper.send_event') as event_mock:
                validation_get_resp_obj = self.app.get(
                    validation_url,
                    headers=RestClientApis.get_json_headers
                )

                # Policy Validation Assert
                validation_get_resp_dict = self.assert_validation(
                    validation_get_resp_obj,
                    POLICY_VALIDATION_GET_RESP_DENIED_UNKNOWN_SESSION,
                    status=HTTPStatus.OK
                )

                assert_event(
                    mlipman_client_dict["client"]["mc_id"],
                    validation_get_resp_dict['response'],
                    event_mock,
                    EventsTest.unknown_policy,
                    alert='warning'
                )
