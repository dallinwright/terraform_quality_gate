#!/usr/bin/env python3
import os
import sys

from modules.call_os_command import call_os_command
from modules.logging import logger
from modules.terratest.terratest_aws import terratest_aws


def main():
    """
    Main program control, here we have entries for each command subset of quality gate.
    The token file containers the credentials for the runner -> terraform cloud authentication
    :return: none
    """
    stage = 'Terraform Format Check (terraform fmt)'
    logger.info('Calling {0}'.format(stage))
    call_os_command(['terraform', '-v'])
    call_os_command(['terraform', 'fmt', '-check'])

    stage = 'Terraform Static Analysis (tflint)'
    logger.info('Calling {0}'.format(stage))
    call_os_command(['tflint', '-v'])
    call_os_command(['tflint'])

    if os.environ.get('TERRATEST') is not None:
        if os.environ.get('TERRATEST').upper() == 'AWS':
            terratest_aws()
            logger.info('terratest aws cloud')

    logger.info('Terraform Quality Gate finished successfully!')
    sys.exit(0)


if __name__ == "__main__":
    main()
