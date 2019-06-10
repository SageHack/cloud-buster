import subprocess

def error_on_target_not_behind_cloudflare():
    exec = subprocess.run(
        args=['python3', 'bust', 'hacklair.cyberguerrilla.org'],
        stdout=subprocess.PIPE
    )

    if exec.returncode != 0:
        print('Error: bad return code')
        print(exec)
        return False

    if 'not behind Cloudflare' not in exec.stdout.decode('utf-8'):
        print('Error: unable to find the expected string')
        print(exec)
        return False

    return True

def test_error_on_target_not_behind_cloudflares():
    assert error_on_target_not_behind_cloudflare() == True
