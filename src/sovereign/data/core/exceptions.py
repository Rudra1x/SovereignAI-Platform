"""
Custom exceptions used by the data platform.
"""


class DataPlatformError(Exception):
    """Base exception."""


class LoaderError(DataPlatformError):
    """Raised when loading fails."""


class ParserError(DataPlatformError):
    """Raised when parsing fails."""


class TransformerError(DataPlatformError):
    """Raised when transformation fails."""


class ValidationError(DataPlatformError):
    """Raised when validation fails."""


class RegistryError(DataPlatformError):
    """Raised when registry lookup fails."""