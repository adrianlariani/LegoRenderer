from subprocess import Popen, PIPE, CalledProcessError


def run_blender(cmd):
    with Popen(cmd, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            if "Fra" not in line:
                print(line, end='')
    if p.returncode != 0:
        raise CalledProcessError(p.returncode, p.args)