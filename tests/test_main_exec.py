import subprocess

def fail_without_args():
    exec = subprocess.run(
        args=['python3', 'bust'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if exec.returncode != 2:
        print('Error: bad return code')
        print(exec)
        return False

    if 'required: DOMAIN' not in exec.stderr.decode('utf-8'):
        print('Error: process does not fail as expected')
        print(exec)
        return False

    return True

def test_fail_without_args():
    assert fail_without_args() == True

def exec_succeed_showing_help():
    exec = subprocess.run(
        args=['python3', 'bust', '-h'],
        stdout=subprocess.PIPE
    )

    if exec.returncode != 0:
        print('Error: bad return code')
        print(exec)
        return False

    if 'usage:' not in exec.stdout.decode('utf-8'):
        print('Error: unable to find expected text')
        print(exec)
        return False

    return True

def test_exec_succeed_showing_help():
    assert exec_succeed_showing_help() == True
