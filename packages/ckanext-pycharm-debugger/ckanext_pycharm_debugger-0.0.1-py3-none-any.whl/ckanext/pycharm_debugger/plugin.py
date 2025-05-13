import os
import sys
import logging


import ckan.plugins as p
from ckan.common import asbool, CKANConfig

log = logging.getLogger(__name__)


class PycharmDebugger(p.SingletonPlugin):
    """Development plugin.

    This plugin provides:
    - Start remote debugger (if correct library is present) during update_config call
    """
    p.implements(p.IConfigurer)

    def update_config(self, config: CKANConfig):

        egg_dir = config.get('debug.remote.egg_dir', None)
        egg_file = config.get('debug.remote.egg_file', None)
        # If we have an egg directory, add the egg to the system path
        # If not set, user is expected to have made pycharm egg findable
        if egg_dir and egg_file:
            log.info("Initiating supplied egg path: %s  file: %s", egg_dir, egg_file)
            sys.path.append(os.path.join(egg_dir, egg_file))

        debug = asbool(config.get('debug.remote', 'False'))
        host_ip = config.get('debug.remote.host.ip', 'host.docker.internal')
        host_port = config.get('debug.remote.host.port', '5678')
        stdout = asbool(config.get('debug.remote.stdout_to_server', 'True'))
        stderr = asbool(config.get('debug.remote.stderr_to_server', 'True'))
        suspend = asbool(config.get('debug.remote.suspend', 'True'))
        if debug:
            # We don't yet have a translator, so messages will be in english only.
            log.info("Initiating remote debugging session to %s:%s", host_ip, host_port)
            try:
                # Not imported on standard build
                import pydevd_pycharm
                pydevd_pycharm.settrace(host_ip, port=int(host_port),
                                        stdoutToServer=stdout,
                                        stderrToServer=stderr,
                                        suspend=suspend)
            except (SystemExit, ConnectionRefusedError):
                log.warning("Failed to connect to debug server; is it started?")

            except (Exception):
                # Catch all other exceptions
                log.warning("debug.enabled set to True, but pydevd_pycharm is missing.")

        else:
            log.info("PyCharm Debugger not enabled")
