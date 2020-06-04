#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import logging
import argparse

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M')


def status_check(rc):
    """
    Verify the status/exit code of each shell command. Exit if anything but 0 is encountered.
    :param rc: number
    :return: none
    """
    if rc != 0:
        logging.error('Exit code: {0}'.format(rc))
        sys.exit(rc)
    else:
        return


def write_token(terraform_token_file, token):
    """
    Write auth token json to terraform config for terraform cloud.
    :param terraform_token_file: string
    :param token: string
    :return: none
    """
    data = {'credentials': {}}
    data['credentials']['app.terraform.io'] = {
        "token": token
    }

    with open(terraform_token_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def call_os_command(command):
    """
    Call OS command, await the async call, check status, and log result.
    :param command: array of strings
    :return: none
    """
    child = subprocess.Popen(command, stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    data = streamdata.decode()
    rc = child.returncode
    status_check(rc)
    if data:
        logging.info(data)
    else:
        return


def main():
    """
    Main program control, here we have entries for each command subset of quality gate
    :return:
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    terraform_token_file = "/github/home/.terraform.d/credentials.tfrc.json"

    parser.add_argument(
        'terratest',
        help='Whether we should include terratests',
        default='none')
    parser.add_argument(
        'token',
        nargs='?',
        help='Cloud authentication token for terraform cloud, required if using terratest full')
    args = parser.parse_args()

    stage = 'Terraform Format Check (terraform fmt)'
    logging.info('Calling {0}'.format(stage))
    call_os_command(['terraform', '-v'])
    call_os_command(['terraform', 'fmt', '-check'])

    stage = 'Terraform Static Analysis (tflint)'
    logging.info('Calling {0}'.format(stage))
    call_os_command(['tflint', '-v'])
    call_os_command(['tflint'])

    if args.terratest == 'full' and args.token:
        logging.info('Writing auth token')
        write_token(terraform_token_file, args.token)

        logging.info('Installing go dependencies')
        call_os_command(
            ['go', 'get', '-v', 'github.com/gruntwork-io/terratest/modules/terraform'])
        call_os_command(
            ['go', 'get', '-v', 'github.com/stretchr/testify/assert'])

        if os.path.isfile(terraform_token_file):
            stage = 'Terraform Integration Testing (terratest)'
            logging.info('Calling {0}'.format(stage))
            call_os_command(['go', 'test', '-v', './tests'])

    sys.exit(0)


if __name__ == "__main__":
    main()
