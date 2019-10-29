#!/usr/bin/env python3
import sys, os, shutil, subprocess

from archive import archive
from get import get
from submit import submit
from test import test
from watch import watch
from list import listCommand
from help import printHelp, helpIfNotCommand
from read import readCommand

# from flags import divideArgs
from ArgsParser import ArgsParser


execCommand = {
    "archive": archive,
    "get": get,
    "submit": submit,
    "test": test,
    "list": listCommand,
    "read": readCommand,
    "watch": watch,
}


def main():

    command = sys.argv[1] if sys.argv[1:] else ""
    args = sys.argv[2:] if sys.argv[2:] else []

    parser = ArgsParser(args)

    parser.parse(listFlags)

    if command == "" or "help" in parser.options:
        printHelp(command)
    elif command in execCommand:
        execCommand[command](parser)
    else:
        helpIfNotCommand(command)


main()
