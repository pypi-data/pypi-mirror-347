import logging
import sys


def setup_logger(verbose: bool = False) -> None:
    if verbose:
        level = "DEBUG"
    else:
        level = "INFO"

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
