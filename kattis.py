#!/usr/bin/env python3
import sys

from commands.work import workCommand
from commands.archive import archiveCommand
from commands.get import getCommand
from commands.submit import submitCommand
from commands.test import testCommand
from commands.watch import watchCommand
from commands.list import listCommand
from commands.help import printHelp, helpIfNotCommand
from commands.read import readCommand
from helpers.flags import divideArgs
from commands.unarchive import unarchiveCommand


execCommand = {
    "archive": archiveCommand,
    "get": getCommand,
    "submit": submitCommand,
    "test": testCommand,
    "list": listCommand,
    "read": readCommand,
    "watch": watchCommand,
    "work": workCommand,
    "unarchive": unarchiveCommand,
}


def main():
    args, options = divideArgs(sys.argv)

    command = args[1] if args[1:] else ""
    args = args[2:] if args[2:] else []

    if command == "" or "help" in options:
        printHelp(command)
    elif command in execCommand:
        execCommand[command](args, options)
    else:
        helpIfNotCommand(command)


main()
