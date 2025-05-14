import logging
import sys


def setup_logger(verbose: bool = False) -> None:
    if verbose:
        logging.basicConfig(
            level="DEBUG",
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )
    else:
        logging.basicConfig(
            level="INFO",
            format="%(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )
