import pytest
from Source import *
from Scheduler import *
from auxiliar import *
from Event import *

import sys
sys.path.append('..')


@pytest.mark.parametrize(
    "source_n, source_bins, expected",
    [
        ([20, 30, 40], [1, 2, 3], sum([20, 30, 40])),
        ([99, 99, 99], [1, 2, 3], sum([99, 99, 99])),
        ([0, 0, 1], [1, 2, 3], 1),
        ([0, 0, 0], [1, 2, 3], 0)
    ]
)
def test_creacio_passatgers(source_n, source_bins, expected):
    scheduler = Scheduler()
    source = Source(scheduler, None, None, None)
    source.n = source_n
    source.bins = source_bins
    for i in range(0, len(source.n)):
        source.ProgramaNovesArribades(i)

    assert source.entitats_creades == expected
