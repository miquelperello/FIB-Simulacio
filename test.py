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
    source = Source(scheduler, None, None, None)
    source.n = source_n
    source.bins = source_bins
    for i in range(0, len(source.n)):
        source.ProgramaNovesArribades(i)

    assert source.entitats_creades == expected


def MostradorLliure():
    ml = Mostradors()
    ml.estat = State.ACTIVE
    return ml


def MostradorOcupat():
    mo = Mostradors()
    mo.estat = State.OCCUPIED
    return mo


@pytest.mark.parametrize(
    "mostradors_config, LlistaMostradorsLliures, expected",
    [
        (3, [MostradorOcupat(), MostradorOcupat(), MostradorOcupat()], 0),
        (3, [MostradorOcupat(), MostradorLliure(), MostradorOcupat()], 1)

    ]
)
def test_mostrador_lliure(mostradors_config, LlistaMostradorsLliures, expected):
    mostradors = Mostradors()
    config = Config()
    config.mostradors = mostradors_config
    mostradors.connecta(None, config, None)
    mostradors.config.mostradors = mostradors_config
    mostradors.LlistaMostradorsLliures = LlistaMostradorsLliures
    assert mostradors.return_mostrador_lliures() == expected


@pytest.mark.parametrize(
    "mostradors_config, LlistaMostradorsLliures, expected",
    [
        (3, [MostradorLliure(), MostradorLliure(),
         MostradorLliure()], 0),
        (3, [MostradorOcupat(), MostradorLliure(),
             MostradorLliure()], 1),
        (3, [MostradorOcupat(), MostradorOcupat(),
             MostradorLliure()], 2),
        (3, [MostradorOcupat(), MostradorOcupat(),
             MostradorOcupat()], None),
    ]
)
def test_elimina_mostrador_lliure(mostradors_config, LlistaMostradorsLliures, expected):
    mostradors = Mostradors()
    config = Config()
    config.mostradors = mostradors_config
    mostradors.connecta(None, config, None)
    mostradors.config.mostradors = mostradors_config
    mostradors.LlistaMostradorsLliures = LlistaMostradorsLliures
    assert mostradors.elimina_mostrador_lliure() == expected


@pytest.mark.parametrize(
    "tid, mostradors, mostradors2, mostradors3, expected",
    [
        (28800, 3, 4, 5, 4),
        (57600, 6, 8, 9, 9),
        (73800, 3, 4, 5, 0),

    ]
)
def test_tractaEvent_Mostrador(tid, mostradors, mostradors2, mostradors3, expected):
    mostradors = Mostradors()
    config = Config()
    config.mostradors = mostradors
    config.mostradors2 = mostradors2
    config.mostradors3 = mostradors3
    mostradors.connecta(None, config, None)
    mostradors.config.mostradors = mostradors

    mEvent = Event(None, tid, EventType.CANVI_DE_TORN)
    mostradors.tractarEsdeveniment(mEvent)
    assert config.mostradors == expected
