#! /usr/bin/python3

#
# Copyright (c) 2015 Cisco Systems, Inc. and others.  All rights reserved.
#
import logging

import requests
import requests.exceptions

# Package imports from local PIP
from magen_logger.logger_config import LogDefaults


def put_url(url, json_req, auth=None, verify=False, headers=None):
    """
    This function performs a PUT request
    :param url: URL used by the PUT request
    :param json_req: The JSON used in the request
    :return: True if checks, otherwise False
    """
    logger = logging.getLogger(LogDefaults.default_log_name)

    try:
        s = requests.Session()
        logger.debug("PUTing {} \n".format(url))
        if headers is None:
            headers = {
                'content-type': 'application/json',
                'accept': 'application/json'}

        r = s.put(url,
                  data=json_req,
                  auth=auth,
                  headers=headers,
                  stream=False,
                  verify=verify,
                  timeout=2.0)

        if r.status_code == 200 or r.status_code == 201:
            return True, "Put success: status %s" % r.status_code
        else:
            logger.error("Put failed with status %s\n", r.status_code)
            return False, "Put failed with status=%s" % r.status_code

    except (requests.exceptions.ConnectionError,
            requests.exceptions.RequestException) as exc:
        logger.error(
            'Failed to PUT configuration. Server might not be running. Error: %s',
            exc)
        return False, "Server might not be running"
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as exc:
        logger.error(
            'Failed to PUT configuration. Server too slow. Error: %s', exc)
        return False, "Server too slow"


def get_url(url, auth=None, verify=False, headers=None):
    """
    This function performs a GET request
    :param url: URL used by the GET request
    :return: True, json_resp if checks, otherwise False, "reason"
    """
    logger = logging.getLogger(LogDefaults.default_log_name)

    try:
        s = requests.Session()
        logger.debug("GETing {} \n".format(url))

        if headers is None:
            headers = {'accept': 'application/json'}

        get_response = s.get(url,
                             auth=auth,
                             stream=False,
                             headers=headers,
                             verify=verify,
                             timeout=1.0)

        if get_response.status_code == 200:
            json_get_resp = get_response.json()
            # json_get_resp = get_response.text
            # magen_logger.debug("Get successful %s\n", json_get_resp)
            return True, json_get_resp
        else:
            logger.debug("Get failed %s\n", get_response.status_code)
            return False, "Get failed with status=%s" % get_response.status_code

    except (requests.exceptions.ConnectionError,
            requests.exceptions.RequestException) as exc:
        # magen_logger.error(
        #     'Failed to GET configuration. Server might not be running. Error: %s',
        #     exc)
        return False, "Server might not be running"

    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as exc:
        # magen_logger.error(
        #     'Failed to GET configuration. Server too slow. Error: %s', exc)
        return False, "Server too slow"


def delete_url(url, json_req=None, auth=None, verify=False, headers=None):
    """
    This function performs a DELETE request
    :param url: URL used by the DELETE request
    :param json_req: The JSON used in the request
    :return: True if checks, otherwise False
    """
    logger = logging.getLogger(LogDefaults.default_log_name)

    try:
        s = requests.Session()
        logger.debug("DELETEing {} \n".format(url))
        if headers is None:
            headers = {
                'content-type': 'application/json',
                'accept': 'application/json'}

        r = s.delete(url,
                     data=json_req,
                     auth=auth,
                     headers=headers,
                     stream=False,
                     verify=verify,
                     timeout=1.0)

        if r.status_code == 200 or r.status_code == 201:
            return True, "Delete success: status %s\n" % r.status_code
        else:
            logger.error("Delete failed with status %s\n", r.status_code)
            return False, "Delete failed with status=%s" % r.status_code

    except (requests.exceptions.ConnectionError,
            requests.exceptions.RequestException) as exc:
        logger.error(
            'Failed to Delete configuration. Server might not be running. Error: %s',
            exc)
        return False, "Server might not be running"
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as exc:
        logger.error(
            'Failed to Delete configuration. Server too slow. Error: %s', exc)
        return False, "Server too slow"
