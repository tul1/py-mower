from abc import ABC, abstractmethod


class MowerPrinterService(ABC):
    pass


class FileMowerPrinterService(MowerPrinterService):
    pass


class StdoutMowerPrinterService(MowerPrinterService):
    pass
