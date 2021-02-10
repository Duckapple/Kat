from argparse import ArgumentParser
from commands.startup import startupParser
from commands.work import workParser
from commands.watch import watchParser
from commands.unarchive import unarchiveParser
from commands.test import testParser
from commands.read import readParser
from commands.list import listParser
from commands.config import configParser
from commands.submit import submitParser
from commands.get import getParser
from commands.archive import archiveParser

parsers = [
    archiveParser,
    configParser,
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
    )
    sub_parsers = parser.add_subparsers(dest='command', metavar='command')

    for p in parsers:
        p(sub_parsers)

    return parser.parse_args(args)