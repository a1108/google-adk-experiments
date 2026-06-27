import logging
import warnings


def configure_logging():
    """
    Configure application logging and suppress non-essential runtime warnings.
    """

    # Configure application logging.
    logging.basicConfig(
        level=logging.ERROR
    )

    # Hide ADK experimental warning.
    warnings.filterwarnings(
        "ignore",
        message=".*JSON_SCHEMA_FOR_FUNC_DECL.*",
    )

    # Hide Google ADC warning.
    warnings.filterwarnings(
        "ignore",
        message=".*authenticated using end user credentials.*",
    )