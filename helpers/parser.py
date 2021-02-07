from argparse import ArgumentParser
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

def parse():
    parser = ArgumentParser(
        description='Get, test and submit Kattis problems.',
    )
    sub_parsers = parser.add_subparsers(dest='command', required=True, metavar='command')

    archiveParser(sub_parsers)
    getParser(sub_parsers)
    submitParser(sub_parsers)
    configParser(sub_parsers)
    listParser(sub_parsers)
    readParser(sub_parsers)
    testParser(sub_parsers)
    unarchiveParser(sub_parsers)
    watchParser(sub_parsers)
    workParser(sub_parsers)

    return parser.parse_args()