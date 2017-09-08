#
# Copyright (c) 2017 Cisco Systems, Inc. and others.  All rights reserved.
#

import logging
import ast

from magen_logger.logger_config import LogDefaults

__author__ = "mlipman"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"

logger = logging.getLogger(LogDefaults.default_log_name)


# read config file in json format, creating dict
def read_dict_from_file(filename):
    s = ""
    try:
        with open(filename, "r") as file:
            s = file.read()
    except IOError:
        logger.warning("Error reading file: %s", filename)
        return {}

    config = ast.literal_eval(s)
    return config
