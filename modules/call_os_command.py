import subprocess
import sys

from modules.logging import logger


def status_check(rc):
    """
    Verify the status/exit code of each shell command. Exit if anything but 0 is encountered.
    :param rc: number
    :return: none
    """
    if rc != 0:
        logger.error('Exit code: {0}'.format(rc))
        sys.exit(rc)
    else:
        return


def call_os_command(command):
    """
    Call OS command, await the async call, check status, and log result.
    :param command: array of strings
    :return: none
    """
    child = subprocess.Popen(command, stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    data = streamdata.decode('utf-8')
    rc = child.returncode
    if data:
        logger.info(data)
        status_check(rc)
    else:
        return
