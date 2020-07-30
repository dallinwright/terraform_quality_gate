from modules.call_os_command import call_os_command
from modules.logging import logger


def terratest():
    stage = 'AWS Terraform Integration Testing (terratest)'
    logger.info('Calling {0}'.format(stage))
    call_os_command(['go', 'test', '-v', './tests'])
