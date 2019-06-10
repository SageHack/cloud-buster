import subprocess
from libtest import bust


def test_match_crimeflare():
    assert bust(
        ['thecatholicdirectory.com', '--scan', 'crimeflare'],
        0, '[match] thecatholicdirectory.com', None
    ) is True
