import glob
import os
import subprocess
import sys

CON_OK = 0


def ssh_connect(user, password, host, port=22):
    proc = subprocess.Popen(
        f'sshpass -p "{password}" ssh {user}@{host} -p {port} exit',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    proc.wait()
    return True if proc.returncode == CON_OK else False

def check_flags(host, port=22):
    levels = glob.glob('level*')

    for level in levels:
        next_level = 'level%02d' % (int(level[5:]) + 1)
        print(level, end=' ')
        flag_path = os.path.join(level, 'flag')

        with open(flag_path) as flag_file:
            flag = flag_file.read().rstrip()

        connection_status = ssh_connect(
            user=next_level,
            password=flag,
            host=host,
            port=port,
        )

        if connection_status:
            print('[OK]')
        else:
            print('KO')


if __name__ == '__main__':
    args = dict(enumerate(sys.argv))
    host = args[1]
    port = int(args.get(2, 4242)) or 4242
    check_flags(host, port)
