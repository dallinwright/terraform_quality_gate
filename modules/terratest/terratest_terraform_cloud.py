import json
import os

from modules.call_os_command import call_os_command
from modules.logging import logger


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


def run_terraform_cloud_terratest():
    terraform_token_file = "/github/home/.terraform.d/credentials.tfrc.json"

    logger.info('Writing auth token')
    write_token(terraform_token_file, os.environ['INPUT_TERRAFORM_CLOUD_TOKEN'])

    if os.path.isfile(terraform_token_file):
        stage = 'Terraform Integration Testing (terratest)'
        logger.info('Calling {0}'.format(stage))
        call_os_command(['go', 'test', '-v', './tests'])
