from typing import Optional, Dict, Tuple

from mower.resources.services.mower_parsers_service import FileMowerParserService
from mower.resources.services.mower_simulations_service import MowerSimulationService
from mower.resources.services.mower_printers_service import MowerPrinterService


class Mower:
    """Mower class"""

    def __init__(self, input_filename: Optional[str] = None, async_sim: Optional[bool] = False, output_filename: Optional[str] = None):
        """Inializer."""
        if input_filename:
            self.mower_parser: MowerParserService = FileMowerParserService(input_filename=input_filename)
        else:
            self.mower_parser: MowerParserService = StdinMowerParserService()

        if async_sim:
            self.mower_simulation: MowerSimulationService = AsyncMowerSimulationService()
        else:
            self.mower_simulation: MowerSimulationService = SyncMowerSimulationService()

        if output_stream:
            self.mower_printer: MowerPrinterService = FileMowerPrinterService(output_filename=output_filename)
        else:
            self.mower_printer: MowerPrinterService = StdoutMowerPrinterService()

    def run(self) -> None:
        """Run method."""
        mowers, lawn = self.mower_parser.parse()
        mower = self.mower_simulation.run(mowers, lawn)
        mower = self.mower_printer.print(mowers)
