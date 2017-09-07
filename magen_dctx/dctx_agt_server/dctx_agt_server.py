# !/bin/usr/python3
"""
Main module for exposing dctx_agt rest apis using a separate
dctx agent process (vs. integrated into policy process).
"""

import argparse
import sys

# Package imports from local PIP
from magen_rest_apis.magen_app import MagenApp
# If this is being run from workspace (as main module),
# import dev/magen_env.py to add workspace package directories.
src_ver = MagenApp.app_source_version(__name__, file="dctx_magen_env")
if src_ver:
    # noinspection PyUnresolvedReferences
    import dev.dctx_magen_env
from magen_mongo_apis.mongo_core_database import LOCAL_MONGO_LOCATOR
from magen_logger.logger_config import LogDefaults, initialize_logger

# Relative imports
from magen_dctx.dctx_lib.dctx_db_lib import dctx_agt_db_init
from magen_dctx.dctx_agt_server.dctx_agt_rest_api import dctx_agt_rest_api_init

__author__ = "gibson@cisco.com"
__copyright__ = "Copyright(c) 2016, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"

DCTX_PORT = 5005

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Magen DCTX Agent',
                                     usage=("\n   python3 dctx_agt_server.py "
                                            "--database "
                                            "--mongo-ip-port <port> "
                                            "--log-dir <dir> "
                                            "--console-log-level {error|info|debug} "
                                            "--clean-init "
                                            "--test\n"))
    parser.add_argument('--database', choices=['Mongo'], default="Mongo",
                        help='Database type such as Mongo or Cassandra '
                             'Default is Mongo')

    parser.add_argument('--mongo-ip-port', default=LOCAL_MONGO_LOCATOR,
                        help='Set Mongo IP and port in form <IP>:<PORT>. '
                             'Default is %s' % LOCAL_MONGO_LOCATOR)

    parser.add_argument('--log-dir', default=LogDefaults.default_dir,
                        help='Set directory for log files.'
                             'Default is %s' % LogDefaults.default_dir)

    parser.add_argument('--console-log-level', choices=['debug', 'info', 'error'],
                        default='error',
                        help='Set log level for console output.'
                             'Default is %s' % 'error')

    parser.add_argument('--clean-init', action='store_false',
                        help='Clean All data when initializing'
                             'Default is to clean)')

    parser.add_argument('--test', action='store_true',
                        help='Run server in test mode. Used for unit tests'
                             'Default is to run in production mode)')

    #: parse CMD arguments ----------------------------------------------------
    args = parser.parse_args()

    logger = initialize_logger(console_level=args.console_log_level, output_dir=args.log_dir)
    logger.setLevel(args.console_log_level.upper())

    app = MagenApp.get_instance().magen

    dctx_agt_rest_api_init(app)
    dctx_agt_db_init(args.mongo_ip_port)

    if args.test:
        app.run(host='0.0.0.0', port=DCTX_PORT, debug=True, use_reloader=False)
    else:
        app.run(host='0.0.0.0', port=DCTX_PORT, threaded=True)

