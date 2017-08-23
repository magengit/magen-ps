#! /usr/bin/python3

#
# Copyright (c) 2015 Cisco Systems, Inc. and others.  All rights reserved.
#

import argparse
import logging
from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS

# Relative imports from local PIP
from magen_datastore_apis.main_db import MainDb
from magen_mongo_apis.mongo_core_database import LOCAL_MONGO_LOCATOR, MongoCore
from magen_logger.logger_config import LogDefaults

__author__ = "mlipman"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"

lctxtest = Flask(__name__)
CORS(lctxtest)


def respond(status, title, response):
    return jsonify({"status": status, "title": title, "response": response})


@lctxtest.route('/', methods=["GET"])
def generic_message():
    return "Welcome to LCTX test server"


@lctxtest.route('/data/', methods=["GET"])
def process_get():
    print(request)
    prepare = "success"
    return respond("200", "Welcome to LCTX test server", prepare)


@lctxtest.route('/data/', methods=["POST","PUT"])
def process_events():
    print("Request:", request)
    events = request.json["notifications"]
    prepare = "success"
    for event in events:
        print("Event:", event, "\n")
        print("Device:", event["deviceId"], "\n")

    return respond("200", "events received", prepare)


def main():
    #: setup parser -----------------------------------------------------------
    parser = argparse.ArgumentParser(description='LCTX Test Server',
                                     usage=("\npython3 server.py "
                                            "--database "
                                            "--mongo-ip-port "
                                            "\n\nnote:\n"
                                            "root privileges are required "))

    parser.add_argument('--database', choices=['Mongo'], default="Mongo",
                        help='Database type such as Mongo or Cassandra '
                             'Default is Mongo')

    parser.add_argument('--mongo-ip-port', default=LOCAL_MONGO_LOCATOR,
                        help='Set Mongo IP and port in form <IP>:<PORT>. '
                             'Default is %s' % LOCAL_MONGO_LOCATOR)

    #: parse CMD arguments ----------------------------------------------------
    args = parser.parse_args()

    if (args.database == "Mongo") and (args.mongo_ip_port is not None):
        # We initialize at runtime everything about Mongo and its functions
        # Any client og the API cna change it later
        db = MainDb.get_instance()
        db.core_database = MongoCore.get_instance()
        db.core_database.db_ip_port = args.mongo_ip_port
        db.core_database.initialize()

    # logger.info("\n\n\n\n ====== STARTING LCTX TEST SERVER  ====== \n")

    lctxtest.run(host='0.0.0.0',port='5003')


if __name__ == "__main__":
    main()
else:
    pass
