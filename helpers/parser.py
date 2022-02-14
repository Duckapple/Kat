from argparse import ArgumentParser
from helpers.config import getConfig

from commands.archive import archiveParser
from commands.config import configParser
from commands.contest import contestParser
from commands.debug import debugParser
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
    debugParser,
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

def parse(args: list = None):
    parser = ArgumentParser(
        description='Get, test and submit Kattis problems.',
        conflict_handler='resolve'
    )
    parser.add_argument('-n', '--no-override', action='store_true', help='Run the command without any of the overrides set in your config.')
    sub_parsers = parser.add_subparsers(dest='command', metavar='command')

    for p in parsers:
        p(sub_parsers)
    

    parsed = vars(parser.parse_args(args))

    noOverride = parsed.get('no_override')
    if noOverride:
        return parsed
    
    cfg = getConfig()
    command = parsed.get('command')
    commandConfig = cfg.get('Default options', {}).get(command, '').strip()

    if commandConfig and args:
        configArgs = commandConfig.split()
        newArgs = unify_args(command, args, configArgs)
        return vars(parser.parse_args(newArgs))
    else:
        return parsed


def unify_args(command, args, configArgs):
    configCommandIndex = configArgs.index(command)
    commandIndex = args.index(command)

    # Filter in command-defined pre-command args
    preCommand = args[ : commandIndex]
    for item in configArgs[ : configCommandIndex]:
        if item not in preCommand:
            preCommand.append(item)

    # Filter in command-defined post-command args
    postCommand = args[commandIndex+1 : ]
    for item in configArgs[configCommandIndex+1 : ]:
        if item not in preCommand:
            postCommand.append(item)

    # Collect them in a single array
    return [*preCommand, command, *postCommand]


