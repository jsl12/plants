import logging

import paramiko

LOGGER = logging.getLogger(__name__)

def get_client(ip: str, username: str, password: str):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    LOGGER.info(f'Connecting to {username}:{password}@{ip}')
    client.connect(ip, username=username, password=password)
    return client


def run(cmd: str, client: paramiko.SSHClient, logging=True):
    LOGGER.info(f'Executing: "{cmd}"')
    stdin, stdout, stderr = client.exec_command(cmd)

    if logging:
        LOGGER.info(f'Capturing stderr:')
        while (line := stderr.readline().strip()):
            print(line)
    else:
        LOGGER.info(f'Capturing stdout:')
        while (line := stdout.readline().strip()):
            print(line)
