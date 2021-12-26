from enum import Enum


class State(Enum):
    SERVICE = 1
    INACTIVE = 2
    ACTIVE = 3
    BUSY = 4
    OCCUPIED = 5
    WAITING = 6
    READY = 7
    PROCESSING = 8


class EventType(Enum):
    SimulationStart = 1
    MOSTRADOR_INICIALITZAT = 2
    NOVA_ARRIBADA = 3
    ENTRA_A_CUA = 4
    PASSATGER_A_MOSTRADOR = 5
    PASSATGER_SURT_MOSTRADOR = 6
    CANVI_DE_TORN = 7
    SimulationEnd = 8


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKRARO = '\033[97m'
    OKGREEN = '\033[92m'
    OKRANDOM = '\033[99m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
