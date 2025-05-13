import logging


def register_command(subparsers):
    parser = subparsers.add_parser(
        "test", help="test command to verify the application is functioning"
    )
    parser.set_defaults(command=handle_test)


def handle_test(args):
    logger = logging.getLogger(__name__)
    logger.info("You called the test command! Everything's working fine")
    logger.debug("(and you have verbose mode turned on)")
