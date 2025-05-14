class ParseError(Exception):
    pass


class InvalidYamlConfigError(Exception):
    pass


class LLMApiError(Exception):
    pass


# retryable
class TransientLLMApiError(Exception):
    pass


class InvalidLLMOutputError(Exception):
    pass


class LocalizationError(Exception):
    pass


class FileSaveError(Exception):
    pass


class LocalizationFormatError(Exception):
    pass


class SerializationError(Exception):
    pass


class UnsupportedLocalizationKeyError(Exception):
    pass


class LocalizationFileAlreadyUpToDateError(Exception):
    pass
