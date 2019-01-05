from pathlib import Path
import ftp
import paramiko

def run_ssh(filename):
    if not isinstance(filename, Path):
        filename = Path.cwd() / filename

    ftp.send_file(filename)
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ftp.IP, username=ftp.USER, password=ftp.PASSWORD)
        stdin, stdout, stderr = ssh.exec_command('python3 {}'.format(filename.name))
        result = stdout.read().decode('ascii').strip()
        error = stderr.read().decode('ascii').strip()
    finally:
        if ssh:
            ssh.close()

    if error != '':
        print(error)
    else:
        print(result)

if __name__ == '__main__':
    run_ssh('plantcam.py')
    ftp.get_pictures()
