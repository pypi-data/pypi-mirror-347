import logging
import sys


def setup_logger(debug: bool = False) -> None:
    if debug:
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
