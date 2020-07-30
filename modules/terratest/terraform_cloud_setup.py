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


def terraform_cloud_setup():
    terraform_token_file = "~/.terraform.d/credentials.tfrc.json"

    logger.info('Writing auth token')
    write_token(terraform_token_file, os.environ['TERRAFORM_CLOUD_TOKEN'])