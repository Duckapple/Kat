from argparse import ArgumentParser

from commands.archive import archiveParser
from commands.config import configParser
from commands.contest import contestParser
from commands.get import getParser
from commands.list import listParser
from commands.read import readParser
from commands.startup import startupParser
from commands.submit import submitParser
from commands.test import testParser
from commands.unarchive import unarchiveParser
from commands.watch import watchParser
from commands.work import workParser

parsers = [
    archiveParser,
    configParser,
    contestParser,
    getParser,
    listParser,
    readParser,
    startupParser,
    submitParser,
    testParser,
    unarchiveParser,
    watchParser,
    workParser,
]

def parse(args = None):
    parser = ArgumentParser(
        description='Get, test and submit Kattis problems.',
        conflict_handler='resolve'
    )
    parser.add_argument('-n', '--no-override', action='store_true', help='Run the command without any of the overrides set in your config.')
    sub_parsers = parser.add_subparsers(dest='command', metavar='command')

    for p in parsers:
        p(sub_parsers)

    return parser.parse_args(args)
