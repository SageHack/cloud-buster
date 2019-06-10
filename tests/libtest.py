import subprocess


def bust(
        args,
        expected_returncode=0,
        expected_stdout=None,
        expected_stderr=None
        ):

    base_args = ['python3', 'bust']
    full_args = base_args + args

    exec = subprocess.run(
        full_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if exec.returncode != expected_returncode:
        print('Error: bad return code')
        print(exec)
        return False

    if expected_stdout is not None:
        if expected_stdout not in exec.stdout.decode('utf-8'):
            print('Error: unable to find the expected string')
            print(exec)
            return False
    else:
        if expected_stdout is not None:
            return False

    if expected_stderr is not None:
        if expected_stderr not in exec.stderr.decode('utf-8'):
            print('Error: process does not fail as expected')
            print(exec)
            return False
    else:
        if expected_stderr is not None:
            return False

    return True
