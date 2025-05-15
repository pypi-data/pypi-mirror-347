#!/usr/bin/env python3

# Copyright 2021-2023 M. Farzalipour Tabriz, Max Planck Computing and Data Facility (MPCDF)
# Copyright 2023-2025 M. Farzalipour Tabriz, Max Planck Institute for Physics (MPP)
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the 3-Clause BSD License. See the LICENSE file for details.

"""
This script spawns a webserver on port 8080 serving files from "./"
without redirecting non-existing {url} to {url}.html

You can pass "SERVER_PORT" "SERVER_PATH" "REDIRECT" "VERBOSITY_LEVEL" variables
[in that order] as cli parameters to modify its default behavior.

"""

import http.server
import os
import socketserver
import sys

from linkmedic.logbook import init_logger


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler with debug level logger and an option
    to redirect missing `page` to `page.html`

    """

    # pylint: disable-next=redefined-builtin
    def log_message(self, format, *args):
        """log webserver messages only at debug

        :param format: log message format
        :param *args: log message arguments

        """
        if "logger_webserver" in globals():
            # pylint: disable-next=possibly-used-before-assignment
            logger_webserver.debug(format, *args)

    def do_GET(self):
        """Get page while selectively redirecting missing pages to .html"""

        # pylint: disable-next=possibly-used-before-assignment
        REDIRECT_MISSING_PAGES = REDIRECT if "REDIRECT" in globals() else False

        if REDIRECT_MISSING_PAGES:
            if not os.path.exists(os.getcwd() + self.path) and os.path.exists(
                os.getcwd() + self.path + ".html"
            ):
                if "logger_webserver" in globals():
                    logger_webserver.debug(
                        "Redirecting: %s -> %s.html", self.path, self.path
                    )
                self.path += ".html"
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


if __name__ == "__main__":
    SERVER_PORT = int(sys.argv[1]) if sys.argv[1:] else 8080
    SERVER_ROOT_PATH = sys.argv[2] if sys.argv[2:] else "./"
    REDIRECT = sys.argv[3] == "True" if sys.argv[3:] else False
    VERBOSITY_LEVEL = int(sys.argv[4]) if sys.argv[4:] else 3

    logger_webserver = init_logger("webserver", VERBOSITY_LEVEL)
    logger_webserver.debug("Requested webserver port       : %s", SERVER_PORT)
    logger_webserver.debug("Requested webserver path       : %s", SERVER_ROOT_PATH)
    logger_webserver.debug("Redirect missing pages to .html: %r", REDIRECT)

    try:
        os.chdir(SERVER_ROOT_PATH)
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", SERVER_PORT), MyHttpRequestHandler) as server:
            server.serve_forever()
    except Exception as server_err:
        logger_webserver.warning(server_err)
        sys.exit(1)
