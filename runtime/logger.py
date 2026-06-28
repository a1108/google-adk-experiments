import logging
import warnings


def configure_logging():
    """
    Configure application logging and suppress non-essential runtime warnings.
    """

    #logging.basicConfig(
    #    level=logging.ERROR,
    #    format="%(levelname)s | %(name)s | %(message)s",
    #)

    logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
    )

    # Enable DEBUG logs only for Google ADK.
    logging.getLogger("google_adk").setLevel(logging.DEBUG)

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