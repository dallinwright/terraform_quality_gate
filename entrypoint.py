#!/usr/bin/env python3
import subprocess
import sys
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')


def status_check(rc):
    if rc != 0:
        logging.error('Exit code: {0}'.format(rc))
        sys.exit(rc)


def call_os_command(command):
    child = subprocess.Popen(command, stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    data = streamdata.decode()
    rc = child.returncode
    status_check(rc)
    if data:
        logging.info(data)


def main():
    stage = 'Terraform Format Check (terraform fmt)'
    logging.info('Calling {0}'.format(stage))
    call_os_command(['terraform', '-v'])
    call_os_command(['terraform', 'fmt', '-check'])

    stage = 'Terraform Static Analysis (tflint)'
    logging.info('Calling {0}'.format(stage))
    call_os_command(['tflint', '-v'])
    call_os_command(['tflint'])


if __name__ == "__main__":
    main()
