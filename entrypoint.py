#!/usr/bin/env python3
import os
import sys

from modules.call_os_command import call_os_command
from modules.logging import logger
from modules.terratest.terratest_aws import terratest_aws
from modules.terratest.terratest_terraform_cloud import terratest_terraform_cloud


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

    if os.environ.get('INPUT_TERRATEST') is not None:
        if os.environ.get('INPUT_TERRATEST').upper() == 'AWS':
            os.environ["AWS_ACCESS_KEY_ID"] = os.environ.get('INPUT_AWS_ACCESS_KEY_ID')
            os.environ["AWS_SECRET_ACCESS_KEY"] = os.environ.get('INPUT_AWS_SECRET_ACCESS_KEY')
            terratest_aws()
        elif os.environ.get('INPUT_TERRATEST').lower() == 'terraform_cloud':
            terratest_terraform_cloud()
        else:
            logger.error('Terratest enabled but no valid cloud provider selected. Please consult README.md')
            sys.exit(1)

    logger.info('Terraform Quality Gate finished successfully!')
    sys.exit(0)


if __name__ == "__main__":
    main()
