# from mower.utils.mower_logger import MowerLogger


class MowerError(Exception):
    """Custom error that is raised from Mower"""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        # MowerLogger().get_logger().error(message)
        super().__init__(message)


class OrdinalDirectionError(MowerError):
    """Custom error that is raised when Mower couldn't load a OrdinalDirection."""

    def __init__(self, value: str, message: str) -> None:
        super().__init__(value, message)


class RelativeDirectionError(MowerError):
    """Custom error that is raised when Mower couldn't load a RelativeDirection."""

    def __init__(self, value: str, message: str) -> None:
        super().__init__(value, message)


class LawnModelLoadError(MowerError):
    """Custom error that is raised when LawnModel couldn't load the Lawn from the input file."""

    def __init__(self, value: str, message: str) -> None:
        super().__init__(value, message)


class MowerModelLoadError(MowerError):
    """Custom error that is raised when MowerModel couldn't load the Mower from the input file."""

    def __init__(self, value: str, message: str) -> None:
        super().__init__(value, message)


class MowerModelError(MowerError):
    """Custom error that is raised when MowerModel coud."""

    def __init__(self, value: str, message: str) -> None:
        super().__init__(value, message)


class LoadFileParserError(MowerError):
    """Custom error that is raised when FileParserService couldn't load correct data from the input file."""

    def __init__(self, value: str, message: str) -> None:
        super().__init__(value, message)
