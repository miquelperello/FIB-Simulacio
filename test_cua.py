import pytest
from Source import *
from Scheduler import *
from auxiliar import *
from Event import *
from collections import Counter
import sys
sys.setrecursionlimit(10000)


c = []


def CuaPassatgers(i):
    global c
    # Netegem per cada crida
    c = []
    for i in range(0, i):
        c.append(Passatger())
    return c


def returnPassatgers(i):
    global c
    return c[i]


def EventBasic():
    return Event(None, 0, None)


def EventCUA(p):
    return Event(None, 10, EventType.ENTRA_A_CUA, p)


@pytest.mark.parametrize(
    "cuaList, entitat, expected",
    [
        (CuaPassatgers(5), returnPassatgers(2), None),
        (CuaPassatgers(1005), returnPassatgers(24), None),
    ]
)
def test_eliminaPassatgerCua(cuaList, entitat,  expected):
    cua = Cua()
    cua.cua = cuaList
    cua.eliminaPassatgerCua(entitat)

    first_or_default = next(
        (x for x in cua.cua if x == entitat), None)
    assert first_or_default == expected


@pytest.mark.parametrize(
    "cuaList, event, mostrador_lliure, expected",
    [
        (CuaPassatgers(5), EventBasic(), 1, returnPassatgers(0)),
        (CuaPassatgers(1005), EventBasic(), 1, returnPassatgers(0)),
        (CuaPassatgers(2), EventBasic(), 1, returnPassatgers(0)),

    ]
)
def test_RecuperaPassatgerCua(cuaList, event, mostrador_lliure, expected):
    scheduler = Scheduler()
    cua = Cua()
    cua.connecta(scheduler, None)
    cua.cua = cuaList
    cua.RecuperaPassatgerCua(event, mostrador_lliure)
    assert (cua.cua[0] != expected)


@pytest.mark.parametrize(
    " event, mostradorslliures, mostradorsocupats, expected",
    [
        (EventCUA(Passatger()), 3, 2, 1),
        (EventCUA(Passatger()), 0, 7, 0),

    ]
)
def test_tractar_ENTRA_A_CUA(event, mostradorslliures, mostradorsocupats, expected):
    # Cas 0 -> Hi ha mostradors lliures, es crea event
    # Cas 1 -> No hi ha mostradors lliures, no es crea i es queda esperant
    scheduler = Scheduler()
    config = Config()
    config.mostradors = mostradorslliures + mostradorsocupats
    mostradors = Mostradors()
    mostradors.connecta(None, config, scheduler)
    mostradors.LlistaMostradorsLliures = []
    cua = Cua()
    cua.connecta(scheduler, mostradors)

    for i in range(0, mostradorslliures):
        m = Mostradors()
        mostradors.LlistaMostradorsLliures.append(m)
    for i in range(0, mostradorsocupats):
        m = Mostradors()
        m.estat = State.OCCUPIED
        mostradors.LlistaMostradorsLliures.append(m)

    # Mirem si es crea event
    comptadorprevis = 0
    comptadoractual = 0
    for i in scheduler.eventList:
        if (i.type == EventType.PASSATGER_A_MOSTRADOR):
            comptadorprevis += 1
    cua.tractarEsdeveniment(event)
    for i in scheduler.eventList:
        if (i.type == EventType.PASSATGER_A_MOSTRADOR):
            comptadoractual += 1
    assert (comptadoractual - comptadorprevis) == expected
