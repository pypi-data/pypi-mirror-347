import argparse
import importlib
import os
import pkgutil

from ..utils import log_utils


class Cli:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="ci-cerberus",
            description=(
                "   🐕 ci-cerberus\n\n"
                "       Scans GitHub workflows for known vulnerable actions using the NIST National Vulnerability Database (NVD) API\n\n"  # noqa: E501
                "       More information on the NVD can be found at https://nvd.nist.gov/developers/vulnerabilities\n"  # noqa: E501
                "       Source code can be found at https://github.com/gavinroderick/ci-cerberus"
            ),
            usage="%(prog)s [options]",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        self._add_help()
        self._add_verbosity()

        # Add subparsers & specify folder location
        self.subparsers = self.parser.add_subparsers(title="commands", metavar="")
        self._add_commands()

    def run(self, args=None):
        parsed_args = self.parser.parse_args(args)

        # Setup logging globally (cli)
        log_utils.setup_logger(parsed_args.verbose)

        if hasattr(parsed_args, "command"):
            parsed_args.command(parsed_args)
        else:
            self.parser.print_help()

    def _add_help(self):
        self.parser.add_argument(
            "-g",
            "--directory",
            type=str,
            metavar="",
            default=".",
            help="Directory where GitHub workflows are located (relative to current directory)",
        )

    def _add_verbosity(self):
        self.parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Enable verbose output (see what's happening under the hood!)",
        )

    def _add_commands(self):
        commands_path = os.path.join(os.path.dirname(__file__), "commands")

        for _, name, _ in pkgutil.iter_modules([commands_path]):
            module = importlib.import_module(f".commands.{name}", package="ci_cerberus.cli")

            if hasattr(module, "register_command"):
                module.register_command(self.subparsers)
