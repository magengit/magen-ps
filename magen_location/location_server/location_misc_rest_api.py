import logging
from http import HTTPStatus

import jinja2
import flask
from flask import request
from magen_logger.logger_config import LogDefaults
from magen_rest_apis.rest_server_apis import RestServerApis

from magen_location.location_server.location_main_rest_api import location_v2
from magen_location.location_libs.location_urls import LocationServerUrls

__author__ = "alifar@cisco.com"
__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.2"
__status__ = "alpha"

loc_misc_server = flask.Blueprint("misc_server", __name__)
logger = logging.getLogger(LogDefaults.default_log_name)


@loc_misc_server.route('/', methods=["GET"])
def index():
    """
    Get root screen for service (on HTTP GET).

      - url - /
    """
    root_page = """
<!DOCTYPE html>
<html lang="en">

<head>
    <title>Welcome to Location</title>
 </head>

<body>
  <div class="container">
    <div>
      <h3 class="text-muted">Magen Location Service</h3>
    </div>
    <p>
      The Magen service that interfaces to external location providers.
    </p>
  <tr>
    <td><a href="html/index.html">Location External Interfaces: Documentation</td>
  </tr>
</body>

</html>"""

    return root_page


@loc_misc_server.route('/html/<path:filename>', methods=["GET"])
def doc(filename):
    """
    Bring up service documentation root page (via HTTP GET).

      - url - /doc/<path:filename>
    """
    location_urls = LocationServerUrls.get_instance()
    if not location_urls.src_version:
        return "             API/CLI documentation currently only available in development run-mode. (This server instance running from installation package.)"
        # in case documentation is ever made available, still will not have src
        # if filename.startswith('_modules/'):
        #     return "         NOTE: Software modules only available when server running from source."

    # development case: render documentation, which must have been built
    doc_template = 'html/' + filename
    try:
        result = flask.render_template(doc_template)
    except jinja2.TemplateNotFound as e:
        logger.error("Exception %s rendering %s.", type(e).__name__, e.message)
        result = "           ERROR: Documentation not currently built. (Build documentation with \"cd policy; make doc\")"

    return result


@loc_misc_server.route('/check/', methods=["GET"])
def heath_check():
    """
    Return a health check result (via HTTP GET).

      - url - /check/

    Useful for health monitoring.

    :return: check success message
    :rtype: string
    """
    return "Check success"


# Deprecate? (Unused)
# @loc_misc_server.route('/data/', methods=["GET"])
def process_get():
    """
    Return a module identification message (via HTTP GET).

      - url - /data/

    :return: welcome message
    :rtype: string
    """
    prepare = "success"
    return RestServerApis.respond(HTTPStatus.OK, "Welcome to LOCATION test server", prepare)


@location_v2.route('/logging_level/', methods=["GET", "POST", "PUT"])
def logging_level():
    """
    Get (via HTTP GET) or set (via HTTP POST/PUT) logging level.

      - url - /magen/location/v2/logging_level/
      - request.json['level'] - level to set (set case only)

    level is either
      - symbolic (debug, info, warn, error, critical)
      - numeric

    :return: http success/failure response with status message
    :rtype: json
    """
    op = "logging_level"
    if request.method == 'GET':
        return RestServerApis.respond(
            HTTPStatus.OK, op,
            {"success": True, "level": logger.getEffectiveLevel()})

    level = request.json.get('level')
    logger.debug("set_logging_level: %s", level)
    if level is None:
        return RestServerApis.respond(
            HTTPStatus.NOT_FOUND, op,
            {"success": False, "cause": "missing required parameters"})

    try:
        _do_set_logging_level(level)

        http_response = RestServerApis.respond(
            HTTPStatus.OK, op, {
                "success": True, "cause": "level set",
                "level": logger.getEffectiveLevel()})
        if request.method == 'POST':
            http_response.headers['location'] = request.url
        return http_response
    except Exception as e:
        return RestServerApis.respond(
            HTTPStatus.INTERNAL_SERVER_ERROR, "logging_level set", {
                "success": False,
                "cause": HTTPStatus.INTERNAL_SERVER_ERROR.phrase})


def _do_set_logging_level(level_str):
    logger = logging.getLogger(LogDefaults.default_log_name)
    if level_str.isnumeric():
        level = int(level_str)
    else:
        level = level_str.upper()

    logger.setLevel(level=level)
    requestsLogger = logging.getLogger("requests")
    requestsLogger.setLevel(level=level)
    werkzeugLogger = logging.getLogger("werkzeug")
    werkzeugLogger.setLevel(level=level)
    return True
