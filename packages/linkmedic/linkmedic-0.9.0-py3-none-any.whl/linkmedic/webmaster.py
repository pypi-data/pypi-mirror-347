# Copyright 2021-2023 M. Farzalipour Tabriz, Max Planck Computing and Data Facility (MPCDF)
# Copyright 2023-2025 M. Farzalipour Tabriz, Max Planck Institute for Physics (MPP)
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the 3-Clause BSD License. See the LICENSE file for details.

import base64
import os
import random
import socket
import subprocess
import sys
import time

import requests

from linkmedic.logbook import init_logger


class MedicServer:
    """contains popen object for the server subprocess
    and information about the server configuration and its status

    """

    is_ready = False
    port = 0
    root_url = ""
    domain = ""
    redirect = False
    process_handle = None
    id = ""
    signature = ""

    def __init__(self, port, root_url, redirect, domain):
        self.port = port
        self.root_url = root_url
        self.redirect = redirect
        self.domain = domain
        self.id = str(random.randrange(sys.maxsize))
        self.signature = (
            base64.urlsafe_b64encode(random.randbytes(16))
            .decode("ASCII")
            .replace("=", "")
            .replace("-", "")
        )

    def __del__(self):
        if self.process_handle:
            self.process_handle.terminate()

    def relative_address(self, url: str):
        """returns address relative to the website root

        :param url:

        """
        return url.replace(self.root_url, "")


def start_webserver(
    requested_port: int = 8080,
    server_root_path: str = "./",
    domain: str = "",
    redirect: bool = True,
    verbosity_level: int = 3,
):
    """Start a webserver. Reconfigure and restart it in case of a failure.

    :param requested_port: requested port (may or may not be available)
    :param server_root_path: path to the local directory to serve the webpages from
    :param domain: domain name for the local webserver
    :param redirect: whether missing `page` should be redirected to `page.html` or not
    :param verbosity_level: logger verbosity level
    :returns: an instance of MedicServer

    """
    newserver = MedicServer(requested_port, server_root_path, redirect, domain)
    server_connection_timeout = 0.5
    CONNECTION_TIMEOUT_MAX = 2
    SERVER_SPAWN_MAX = 100
    logger_webmaster = init_logger("webmaster", verbosity_level)

    server_signature_file_path = os.path.join(server_root_path, newserver.signature)
    try:
        with open(server_signature_file_path, "w", encoding="ascii") as signature_file:
            signature_file.write(newserver.id)
    except IOError as write_error:
        logger_webmaster.warning("Cannot write to the webserver root path!")
        logger_webmaster.warning(write_error)
        logger_webmaster.warning("Server verification will be skipped!")
        newserver.signature = ""
        newserver.id = ""

    # Try to start a webserver
    server_spawn_count = 1
    while not newserver.is_ready and server_spawn_count < SERVER_SPAWN_MAX:
        logger_webmaster.debug("Checking port %d", newserver.port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_socket:
            test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if test_socket.connect_ex(("localhost", newserver.port)) == 0:
                logger_webmaster.info("Port %d is not avaiable!", newserver.port)
                newserver.port += 1
                continue
            logger_webmaster.debug("Port %d seems to be free!", newserver.port)

        newserver.root_url = "http://localhost:" + str(newserver.port)
        logger_webmaster.info("Starting test webserver on port %d", newserver.port)
        newserver.process_handle = (
            subprocess.Popen(  # pylint: disable=consider-using-with
                [
                    sys.executable,
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), "webserver.py"
                    ),
                    str(newserver.port),
                    server_root_path,
                    str(newserver.redirect),
                    str(verbosity_level),
                ],
            )
        )
        time.sleep(server_connection_timeout)

        try:
            server_exit = newserver.process_handle.poll()
            if server_exit:
                raise ChildProcessError(
                    "Webserver exited unexpectedly! Exit code: " + str(server_exit)
                )
            response = requests.get(
                newserver.root_url + "/" + newserver.signature,
                timeout=server_connection_timeout,
            )
            if newserver.id:
                response.encoding = "ascii"
                if response.text == newserver.id:
                    logger_webmaster.info("Webserver started!")
                    newserver.is_ready = True
                    os.unlink(server_signature_file_path)
                else:
                    logger_webmaster.info("Webserver could not be started!")
                    logger_webmaster.debug("Connected server ID: %s", response.text)
            else:
                newserver.is_ready = True
        except Exception as startup_err:
            server_spawn_count += 1
            logger_webmaster.debug(startup_err)
            newserver.process_handle.terminate()
            newserver.port += 1
            if server_connection_timeout < CONNECTION_TIMEOUT_MAX:
                server_connection_timeout += 0.1
                logger_webmaster.debug(
                    "Connection timeout adjusted to %0.1f s", server_connection_timeout
                )
        if server_spawn_count >= SERVER_SPAWN_MAX:
            logger_webmaster.error(
                "Maximum retries reached. Could not spawn the webserver!"
            )
            sys.exit(1)
    return newserver
