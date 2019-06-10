import subprocess
from libtest import bust


def test_fail_without_args():
    assert bust(
        [], 2, None, 'required: DOMAIN'
    ) is True


def test_show_help():
    assert bust(
        ['-h'], 0, 'usage:', None
    ) is True

def test_unresolvable_domain():
    assert bust(
        ['buster-test-9000.tk'], 0, 'cannot resolve host', None
    ) is True

def test_target_not_behind_cloudflares():
    assert bust(
        ['hacklair.cyberguerrilla.org'], 0, 'not behind Cloudflare', None
    ) is True

