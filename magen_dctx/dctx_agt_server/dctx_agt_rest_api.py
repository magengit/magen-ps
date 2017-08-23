# !/bin/usr/python3
"""
ReST HTTP request handlers
"""

from http import HTTPStatus
from flask import request, Blueprint

# Package imports from local PIP
from magen_rest_apis.rest_server_apis import RestServerApis

# Relative imports
from magen_dctx.dctx_agt_apis.dctx_state_api import DctxState

__author__ = "gibson@cisco.com"
__copyright__ = "Copyright(c) 2017, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"

# dctx_states

dctx_states = Blueprint("dctx_states", __name__)

# dctx (2017-05-20)
#
#
#         post   /magen/dctx/v1/states/state/
#         get    /magen/dctx/v1/states/state/{dc_id}/
#         get    /magen/dctx/v1/states/device/{device_id}/
#         get    /magen/dctx/v1/states/user/{username}/
#         get    /magen/dctx/v1/states/
#         del    /magen/dctx/v1/states/state/{dc_id}/
#         del    /magen/dctx/v1/states/device/{device_id}/
#         del    /magen/dctx/v1/states/user/{username}/
#         del    /magen/dctx/v1/states/


def dctx_agt_rest_api_init(flask_app):
    """
    Register rest handlers

    Internal API called at service boot time by a service that
    is supporting these rest apis.
    """
    flask_app.register_blueprint(
        dctx_states, url_prefix='/magen/dctx/v1/states')


@dctx_states.route('/state/', methods=["POST"])
def dctx_agt_rest_api_update():
    """
    Update dctx state (via HTTP POST)

      - url - /magen/dctx/v1/state/
      - request.json['magen_dctx_update']['device_states'] - single-element list of dctx states

    :return: http success/failure response with status message
    :rtype: json
    """
    try:
        states = request.json['magen_dctx_update']['device_states']
        assert len(states) == 1, "upsert-multiple: rest api currently supports only a single record"
            
        update_dict = request.json['magen_dctx_update']['device_states'][0]
        success, dc_id, response = DctxState.process_update(update_dict)
    except Exception as e:
        success = False
        response = None

    result = dict(
        success=success,
        device_states=response
    )
    if success:
        result['cause'] = ""
        http_status = HTTPStatus.OK
    else:
        result['cause'] = "State Update Failed"
        http_status = HTTPStatus.NOT_FOUND
    http_response = RestServerApis.respond(http_status, "Dctx State Update", response)
    if success:
        http_response.headers['location'] = request.url + dc_id + "/"
    return http_response


#
# Some implementations may set device_id to username and restrict
# to a single device context per user.
#
@dctx_states.route('/state/<dc_id>/', methods=["GET"])
def dctx_agt_rest_api_get_one_by_dc_id(dc_id):
    """
    Get one dctx_state record by dc_id (via HTTP GET)

      - url - /magen/dctx/v1/<dc_id>/

    :param dc_id: dc identifier for existing state record
    :type dc_id: dc_id str 
    :return: http success/failure, with single-element list of dctx states if successful.
    :rtype: json
    """
    success, response = DctxState.get_one_by_dc_id(dc_id=dc_id)
    result = dict(
        success=success,
        device_states=response
    )
    if success:
        result['cause'] = ""
        http_status = HTTPStatus.OK
    else:
        result['cause'] = "State Not found"
        http_status = HTTPStatus.NOT_FOUND
    return RestServerApis.respond(http_status, "Dctx State(s)", result)


#
# Some implementations may set device_id to username and restrict
# to a single device context per user.
#
@dctx_states.route('/device/<device_id>/', methods=["GET"])
def dctx_agt_rest_api_get_one_by_device_id(device_id):
    """
    Get one device record by device_id (via HTTP GET)

      - url - /magen/dctx/v1/<device_id>/

    :param device_id: device identifier for existing state record
    :type device_id: device_id str 
    :return: http success/failure, with single-element list of dctx states if successful.
    :rtype: json
    """
    success, response = DctxState.get_one_by_device_id(device_id)
    result = dict(
        success=success,
        device_states=response
    )
    if success:
        result['cause'] = ""
        http_status = HTTPStatus.OK
    else:
        result['cause'] = "State Not found"
        http_status = HTTPStatus.NOT_FOUND
    return RestServerApis.respond(http_status, "Dctx State(s)", result)
    

@dctx_states.route('/user/<username>/', methods=["GET"])
def dctx_agt_rest_api_get_all_by_username(username):
    """
    Get all dctx_state records by username (via HTTP GET)

      - url - /magen/dctx/v1/user/<username>/

    :param username: username identifier for existing state records
    :type username: str 
    :return: http success/failure, with list of dctx states if successful.
    :rtype: json
    """
    success, response = DctxState.get_all_by_username(username=username)
    if response:
        result = dict(
            success=True,
            device_states=response,
            cause=""
        )
    else:
        result = dict(
            success=False,
            device_states=response,
            cause="No states found"
        )
    http_status = HTTPStatus.OK
    return RestServerApis.respond(http_status, "Dctx State(s)", result)


@dctx_states.route('/', methods=["GET"])
def dctx_agt_rest_api_get_all():
    """...
    Get all dctx_state records (via HTTP GET)

      - url - /magen/dctx/v1/

    :return: http success/failure, with list of dctx states if successful.
    :rtype: json
    """
    success, response = DctxState.get_all()
    if response:
        result = dict(
            success=True,
            device_states=response,
            cause=""
        )
    else:
        result = dict(
            success=False,
            device_states=response,
            cause="No states found"
        )
    http_status = HTTPStatus.OK
    return RestServerApis.respond(http_status, "Dctx States", result)

@dctx_states.route('/state/<dc_id>/', methods=["DELETE"])
def dctx_agt_rest_api_delete_one_by_dc_id(dc_id):
    """...
    Delete one dctx_state record by dc_id (via HTTP DELETE)

      - url - /magen/dctx/v1/<dc_id>/

    :param dc_id: dc identifier for existing state record
    :type dc_id: dc_id str 
    :return: http success/failure response with status message
    :rtype: json
    """
    success, response = DctxState.delete_one_by_dc_id(dc_id)
    result = dict(
        success=success,
        device_states=response
    )
    if success:
        result['cause'] = ""
        http_status = HTTPStatus.OK
    else:
        result['cause'] = "State Not found"
        http_status = HTTPStatus.NOT_FOUND
    return RestServerApis.respond(http_status, "Dctx Delete State", result)


@dctx_states.route('/device/<device_id>/', methods=["DELETE"])
def dctx_agt_rest_api_delete_one_by_device_id(device_id):
    """
    Delete one device record by device_id (via HTTP DELETE)

      - url - /magen/dctx/v1/<device_id>/

    :param device_id: device identifier for existing state record
    :type device_id: device_id str 
    :return: http success/failure response with status message
    :rtype: json
    """
    success, response = DctxState.delete_one_by_device_id(device_id)
    result = dict(
        success=success,
        device_states=response
    )
    if success:
        result['cause'] = ""
        http_status = HTTPStatus.OK
    else:
        result['cause'] = "State Not found"
        http_status = HTTPStatus.NOT_FOUND
    return RestServerApis.respond(http_status, "Dctx Delete State", result)


@dctx_states.route('/user/<username>/', methods=["DELETE"])
def dctx_agt_rest_api_delete_all_by_username(username):
    """...
    Delete all dctx_state records by username (via HTTP DELETE)

      - url - /magen/dctx/v1/<username>/

    :param username: username identifier for existing state records
    :type username: str 
    :return: http success/failure response with status message
    :rtype: json
    """
    success, response = DctxState.delete_all_by_username(username)
    result = dict(
        success=success,
        device_states=response
    )
    if success:
        result['cause'] = ""
        http_status = HTTPStatus.OK
    else:
        result['cause'] = "State Not found"
        http_status = HTTPStatus.NOT_FOUND
    return RestServerApis.respond(http_status, "Dctx Delete States", result)


@dctx_states.route('/', methods=["DELETE"])
def dctx_agt_rest_api_delete_all():
    """...
    Delete all dctx_state records (via HTTP DELETE)

      - url - /magen/dctx/v1/

    :return: http success/failure response with status message
    :rtype: json
    """
    success, db_return = DctxState.delete_all()
    http_status = HTTPStatus.OK if db_return.success else HTTPStatus.INTERNAL_SERVER_ERROR

    return RestServerApis.respond(http_status, "Dctx Delete States",
                                  {"success": db_return.success,
                                   "cause": db_return.message})
