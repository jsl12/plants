from pathlib import Path
import ftp
import paramiko

def run_ssh(script_name, **kwargs):
    if not isinstance(script_name, Path):
        script_name = Path.cwd() / script_name

    cmd = 'python3 '
    if len(kwargs) > 0:
        cmd += '{} '.format(script_name.name)
        cmd += ' '.join(['--{} {}'.format(arg, kwargs[arg]) for arg in kwargs])
    else:
        cmd += script_name.name

    ftp.send_file(script_name)
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ftp.IP, username=ftp.USER, password=ftp.PASSWORD)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read().decode('ascii').strip()
        error = stderr.read().decode('ascii').strip()
    finally:
        if ssh:
            ssh.close()

    if error != '':
        for line in error.splitlines():
            print(line)
    else:
        for line in result.splitlines():
            print(line)

if __name__ == '__main__':
    # run_ssh('plantcam.py', filename='test.jpg', timestamp=True)
    run_ssh('timelapse.py')
    ftp.get_pictures()
