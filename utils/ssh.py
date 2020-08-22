import logging

import paramiko

LOGGER = logging.getLogger(__name__)

def get_client(ip: str, username: str, password: str):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    LOGGER.info(f'Connecting to {ip} with {username}:{password}')
    client.connect(ip, username=username, password=password)
    return client


def run(cmd: str, client: paramiko.SSHClient):
    LOGGER.info(f'Executing: "{cmd}"')
    stdin, stdout, stderr = client.exec_command(cmd)
    result = stdout.read().decode('ascii').strip()
    error = stderr.read().decode('ascii').strip()
    if error != '':
        for line in error.splitlines():
            print(line)
    else:
        for line in result.splitlines():
            print(line)
