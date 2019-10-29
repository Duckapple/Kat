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
from flags import divideArgs


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
    args, options = divideArgs(sys.argv)

    command = args[1] if args[1:] else ""
    args = args[2:] if args[2:] else []

    if command == "" or "-h" in options:
        printHelp(command)
    elif command in execCommand:
        execCommand[command](args, options)
    else:
        helpIfNotCommand(command)


main()
