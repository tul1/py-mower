from mower.resources.services.mower_parsers_service import FileMowerParserService


class Mower:
    """Mower class"""

    def __init__(self, filename: str):
        self.mower_parser: FileMowerParserService = FileMowerParserService(filename)

    def run(self) -> None:
        """."""
        mowers, lawn = self.mower_parser.parse()
        # Simulate