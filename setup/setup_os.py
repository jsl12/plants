import shutil
from pathlib import Path

import paramiko


def enable_ssh(BOOT_VOLUME):
    filename = 'ssh.txt'
    source = Path.cwd() / filename
    dest = BOOT_VOLUME / filename
    shutil.copyfile(source, dest)
    print('Moved {} to {}'.format(source.name, dest))

def setup_wifi(BOOT_VOLUME):
    filename = 'wpa_supplicant.conf'
    source = Path.cwd() / filename
    dest = BOOT_VOLUME / filename
    shutil.copyfile(source, dest)
    print('Moved {} to {}'.format(source.name, dest))

def setup_os(BOOT_VOLUME):
    enable_ssh(BOOT_VOLUME)
    setup_wifi(BOOT_VOLUME)

def remote_script(ip, username, password, script):
    if not isinstance(script, Path):
        Path.cwd() / script

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        with open(script, 'rb') as file:
            for line in file.readlines():
                line = line.strip().decode('ascii')
                print('~ $ {}'.format(line))
                stdin, stdout, stderr = ssh.exec_command(line)

                result = stdout.read().decode('ascii').strip()
                error = stderr.read().decode('ascii').strip()
                if error != '':
                    for line in error.splitlines():
                        print(line)
                else:
                    for line in result.splitlines():
                        print(line)
    finally:
        if ssh:
            ssh.close()

if __name__ == '__main__':
    setup_os(Path(r'E:\\'))
    # remote_script('192.168.1.126', 'pi', 'raspberry', 'picam-setup.sh')


