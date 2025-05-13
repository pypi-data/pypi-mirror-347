"Custom exceptions for dsloader"


class DSLoaderBaseException(Exception):
    """DSLoader base exception class."""


class WrongSMARTDSPrefix(DSLoaderBaseException):
    """Raise this error if non existent prefix is passed
    when downloading SMARTDS dataset."""


class FolderAlreadyExistsError(DSLoaderBaseException):
    """Raise this error if folder already exists to avoid accidental overwrite."""
