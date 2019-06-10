import subprocess

def error_on_target_not_behind_cloudflare():
    return subprocess.run(
        args=['python3', 'bust', 'hacklair.cyberguerrilla.org'],
        stdout=subprocess.PIPE
    )

def test_error_on_target_not_behind_cloudflares():
    process = error_on_target_not_behind_cloudflare()
    print(process)
    stdout = process.stdout.decode("utf-8")
    assert stdout.find('not behind Cloudflare')
