from Source import *
from Scheduler import *
from auxiliar import *
from Event import *
import pytest
import sys


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
    cua = Cua()
    config.mostradors = mostradors
    config.mostradors2 = mostradors2
    config.mostradors3 = mostradors3
    mostradors.connecta(cua, config, None)
    mostradors.config.mostradors = mostradors

    mEvent = Event(None, tid, EventType.CANVI_DE_TORN)
    mostradors.tractarEsdeveniment(mEvent)
    assert config.mostradors == expected


@pytest.mark.parametrize(
    "mostrador_assignat, LlistaMostradorsLliures, expected",
    [

        (0, [MostradorOcupat(), MostradorLliure(),
             MostradorLliure()], State.ACTIVE),
        (2, [MostradorOcupat(), MostradorOcupat(),
             MostradorLliure()], State.ACTIVE),
        (1, [MostradorLliure(), MostradorLliure(),
             MostradorLliure()], State.ACTIVE),
    ]
)
def test_afegeix_mostrador_lliure(mostrador_assignat, LlistaMostradorsLliures, expected):
    mostradors = Mostradors()
    mostradors.LlistaMostradorsLliures = LlistaMostradorsLliures
    passatger = Passatger()
    passatger.mostrador_assignat = 0
    pe = Event(None, 0, None, passatger)
    config = Config()
    mostradors.afegeix_mostrador_lliure(pe)
    assert mostradors.LlistaMostradorsLliures[mostrador_assignat].estat == expected
