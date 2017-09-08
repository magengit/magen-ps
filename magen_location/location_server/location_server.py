#! /usr/bin/python3

#
# Copyright (c) 2015 Cisco Systems, Inc. and others.  All rights reserved.
#
import argparse
import sys
import logging

import flask
from flask_cors import CORS

# Package imports from local PIP
from magen_rest_apis.magen_app import MagenApp
# If this is being run from workspace (as main module),
# import dev/magen_env.py to add workspace package directories.
src_ver = MagenApp.app_source_version(__name__)
if src_ver:
    # noinspection PyUnresolvedReferences
    import dev.magen_env
from magen_logger.logger_config import LogDefaults
from magen_logger.logger_config import initialize_logger
from magen_utils_apis import domain_resolver
from magen_rest_apis.rest_server_apis import RestServerApis
from magen_rest_apis.server_urls import ServerUrls


# Relative imports
from magen_location.location_libs.location_urls import LocationServerUrls
from magen_location.location_libs.location_utils import get_url
from magen_location.location_libs.location_dbthread import CustomJSONEncoder, _ls_spawn_database_update_thread
from magen_location.location_server.location_lctx_rest_api import location_lctx_v2
from magen_location.location_server.location_misc_rest_api import loc_misc_server
from magen_location.location_server.location_main_rest_api import location_v2

from magen_dctx.dctx_lib.dctx_db_lib import dctx_agt_db_init
from magen_dctx.dctx_agt_server.dctx_agt_rest_api import dctx_agt_rest_api_init

__author__ = "mlipman"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"

logger = logging.getLogger(LogDefaults.default_log_name)

locationServer = flask.Flask(__name__)
locationServer.json_encoder = CustomJSONEncoder
CORS(locationServer)

# FIXME:
# check the following cases
# configuration of micro-service and LCTX server ip/port, other config parameters
# remove policies - validators should be removed (garbage collected or removed based on MB message)
# update policies - validators should be updated
# support policy server location and separate micro-service for backwards support of demo
# support scale out of location micro-service
#   need to manage changes to the PI in the database from multiple services
# configuration of micro-service and LCTX server ip/port, other config parameters from environment
#   find LCTX via DNS resolution

SERVER_HOST = "0.0.0.0"
POLICY_HOST = "0.0.0.0"
# FIXME: if LCTX_SERVER_LOCATION is 0.0.0.0 then treat as a no-op (for
# testing without LCTX)
LCTX_SERVER_LOCATOR = "0.0.0.0"


def _ls_test_mode_locator(production_mode_locator):
    """
    Return locator (host[:port]), updated for test mode operation.

    Add _test to host portion of locator, e.g. convert magen_policy:5000
    to magen_policy_test:5000
    """
    if not domain_resolver.inside_docker():
        return production_mode_locator
    locator_components = production_mode_locator.split(':')
    locator_components[0] += '_test'
    return ':'.join(locator_components)


def _ls_test_mode_url_locators_update_defaults():
    """
    Update, for test mode operation, the locators returned by ServerUrls urls

    For the two components (policy, location) cooperating in test mode,
    extract the locator from ServerUrls, convert to the corresponding
    test mode locator, and update ServerUrls locator.

    The updated value will flow through to affect the authority portion
    of the urls returned for those components.
    """
    server_urls = ServerUrls.get_instance()
    policy_dflt_locator = server_urls.policy_server_url_host_port
    policy_test_locator = _ls_test_mode_locator(policy_dflt_locator)
    if policy_test_locator != policy_dflt_locator:
        server_urls.set_policy_server_url_host_port(policy_test_locator)

    location_dflt_locator = server_urls.location_server_url_host_port
    location_test_locator = _ls_test_mode_locator(location_dflt_locator)
    if location_test_locator != location_dflt_locator:
        server_urls.set_location_server_url_host_port(location_test_locator)


def main():
    # NOTE: docstring content below was generated using non-default columns:
    #  bash$ COLUMNS=70 policy_server.py --help
    """
    Run location server, with following command line options::

      bash$ location_server.py --help
      usage:
        python3 location_server.py \\
            --mongo-ip-port <port> \\
            --pdp-server-ip-port <port> \\
            --lctx-server-ip-port <port> \\
            --location-server-ip-port <port>
            --test

      LCTX Test Server

      optional arguments:
        -h, --help            show this help message and exit
        --mongo-ip-port MONGO_IP_PORT
                              Set Mongo IP and port in form <IP>:<PORT>.
                              Default is 127.0.0.1:27017
        --pdp-server-ip-port PDP_SERVER_IP_PORT
                              Set PDP SERVER IP and port in form
                              <IP>:<PORT>. Default is 0.0.0.0:5000
        --lctx-server-ip-port LCTX_SERVER_IP_PORT
                              Set LCTX IP and port in form <IP>:<PORT>.
                              Default is 0.0.0.0
        --location-server-ip-port LOCATION_SERVER_IP_PORT
                              Set LOCATION IP and port in form
                              <IP>:<PORT>. Default is 0.0.0.0:5003
        --log-dir LOG_DIR     Set directory for log files.Default is
                              /Users/gibson/gibson-docs/Cisco/Pken/Magen/C
                              ode/_magen.v1/magen_1205/magen-
                              psdoc/location/magen_logs/
        --console-log-level {debug,info,error}
                              Set log level for console output. Default is
                              error
        --service-instance-name SERVICE_INSTANCE_NAME
                              Service instance name, must be unique. Default
                              is <hostname>:5003
        --test                Run server in test mode. Used for unit
                              testsDefault is to run in production mode)
    """
    location_urls = LocationServerUrls.get_instance()
    location_urls.src_version = src_ver
    server_urls = ServerUrls.get_instance()
    location_server_locator = SERVER_HOST + ':' + str(server_urls.location_port)
    policy_server_locator = POLICY_HOST + ':' + str(server_urls.policy_port)
    cons_debug_default='error'

    #: setup parser -----------------------------------------------------------
    parser = argparse.ArgumentParser(description='LCTX Test Server',
                                     usage=("\npython3 location_server.py "
                                            "--mongo-ip-port <port> "
                                            "--pdp-server-ip-port <port> "
                                            "--lctx-server-ip-port <port> "
                                            "--location-server-ip-port <port> "
                                            "--test\n"))

    parser.add_argument('--mongo-ip-port',
                        help='Set Mongo IP and port in form <IP>:<PORT>. '
                             'Default is %s' % domain_resolver.LOCAL_MONGO_LOCATOR)

    parser.add_argument(
        '--pdp-server-ip-port',
        default=policy_server_locator,
        help='Set PDP SERVER IP and port in form <IP>:<PORT>. '
             'Default is %s' % policy_server_locator)

    parser.add_argument('--lctx-server-ip-port', default=LCTX_SERVER_LOCATOR,
                        help='Set LCTX IP and port in form <IP>:<PORT>. '
                             'Default is %s' % LCTX_SERVER_LOCATOR)

    parser.add_argument(
        '--location-server-ip-port',
        default=location_server_locator,
        help='Set LOCATION IP and port in form <IP>:<PORT>. '
             'Default is %s' % location_server_locator)

    parser.add_argument(
        '--log-dir',
        default=LogDefaults.default_dir,
        help='Set directory for log files.'
             'Default is %s' % LogDefaults.default_dir)

    parser.add_argument(
        '--console-log-level',
        choices=[
            'debug',
            'info',
            'error'],
        default=cons_debug_default,
        help='Set log level for console output. '
             'Default is %s' % cons_debug_default)

    parser.add_argument('--test', action='store_true',
                        help='Run server in test mode. Used for unit tests'
                             'Default is to run in production mode)')

    #: parse CMD arguments ----------------------------------------------------
    args = parser.parse_args()
    test_mode = args.test
    if test_mode:
        _ls_test_mode_url_locators_update_defaults()

    mongo_locator = args.mongo_ip_port if args.mongo_ip_port else domain_resolver.mongo_locator()

    initialize_logger(
        console_level=args.console_log_level,
        output_dir=args.log_dir,
        logger=logger)
    logger.setLevel(args.console_log_level.upper())
    logger.info("LOCATION LOGGING LEVEL: %s(%s)", args.console_log_level, logger.getEffectiveLevel())

    pdp_server_ip_port = args.pdp_server_ip_port
    if domain_resolver.inside_docker():
        policy_port = str(server_urls.policy_port)
        if policy_port not in pdp_server_ip_port:
            pdp_server_ip_port += ":" + policy_port
    logger.info("pdp server from args: %s", pdp_server_ip_port)
    location_urls.set_pdp_server_url_host_port(pdp_server_ip_port)

    dctx_agt_db_init(mongo_locator)

    print("\n\n\n\n ====== STARTING LOCATION SERVER  ====== \n")
    sys.stdout.flush()

    logger.info("Setting up LCTX address and authorization info...\n")
    logger.info(
        "log level=%s, log dir=%s\n",
        args.console_log_level,
        args.log_dir)

    logger.info("lctx server: %s", args.lctx_server_ip_port)
    location_urls.set_lctx_server_url_host_port(args.lctx_server_ip_port)
    location_urls.basic_auth_arguments = ('admin', 'Public123')
    location_urls.notification_server_userid = "admin"

    logger.info("location server: %s", args.location_server_ip_port)
    location_urls.local_server_host_port = args.location_server_ip_port

    app = locationServer
    pfx = location_urls.location_v2_url_pfx
    app.register_blueprint(location_v2, url_prefix=pfx)
    app.register_blueprint(loc_misc_server)
    app.register_blueprint(location_lctx_v2, url_prefix=pfx + '/lctx')

    dctx_agt_rest_api_init(locationServer)

    RestServerApis.rest_api_log_all(app)

    logger.info("Starting database update thread...\n")

    # start this explicitly
    _ls_spawn_database_update_thread("main")

    if not test_mode:
        location_urls.location_doc_dir_set(app)
    app.run(host=SERVER_HOST, port=server_urls.location_port, threaded=True)

if __name__ == "__main__":
    main()
else:
    pass
