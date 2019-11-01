#!/usr/bin/env python3
import sys

from commands.work import workCommand
from commands.archive import archive
from commands.get import get
from commands.submit import submit
from commands.test import test
from commands.watch import watch
from commands.list import listCommand
from commands.help import printHelp, helpIfNotCommand
from commands.read import readCommand
from helpers.flags import divideArgs


execCommand = {
    "archive": archive,
    "get": get,
    "submit": submit,
    "test": test,
    "list": listCommand,
    "read": readCommand,
    "watch": watch,
    "work": workCommand,
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
