import pytest
from Source import *
from Scheduler import *
from auxiliar import *
from Event import *


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
    source = Source()
    source.connecta(scheduler, None, None, None)
    source.n = source_n
    source.bins = source_bins
    for i in range(0, len(source.n)):
        source.ProgramaNovesArribades(i)

    assert source.entitats_creades == expected


@pytest.mark.parametrize(
    "passatgers, expected",
    [
        (150, 150),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (10, 10),
        (15, 15),
        (16, 16),
        (30, 30),
        (20, 20),
        (50, 50),

    ]
)
def test_GenerateDistribution(passatgers, expected):
    scheduler = Scheduler()
    source = Source()
    config = Config()
    source.connecta(scheduler, config, None, None)
    source.config.passatgers = passatgers
    source.GenerateDistribution()
    assert passatgers == sum(source.n)


@pytest.mark.parametrize(
    "m1, m2, m3, expected",
    [
        (2, 5, 8, 8),
        (1, 2, 2, 2),
        (4, 4, -3, 4),
        (0, 0, 0, 0)
    ]
)
def test_inicialitzaMostradors(m1, m2, m3, expected):
    scheduler = Scheduler()
    source = Source()
    config = Config()
    source.connecta(scheduler, config, None, None)

    config.mostradors1 = m1
    config.mostradors2 = m2
    config.mostradors3 = m3
    source.config = config
    # Dividim entre abans i després, ja que al cridar a scheduler, inicialitza mostradors
    comptadorprevis = 0
    comptadoractual = 0
    for i in scheduler.eventList:
        if (i.type == EventType.MOSTRADOR_INICIALITZAT):
            comptadorprevis += 1
    source.inicialitzaMostradors()
    for i in scheduler.eventList:
        if (i.type == EventType.MOSTRADOR_INICIALITZAT):
            comptadoractual += 1
    assert (comptadoractual - comptadorprevis) == expected
