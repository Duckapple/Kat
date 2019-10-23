#!/usr/bin/env python3
import sys, os, shutil, subprocess

from archive import archive
from get import get
from submit import submit
from test import test
from list import listCommand
from help import printHelp, helpIfNotCommand


def divideArgs(args):
    arg = []
    options = []
    for word in args:
        if "-" in word:
            options.append(word)
        else:
            arg.append(word)
    return arg, options


execCommand = {"archive": archive, "get": get, "submit": submit, "test": test, "list": listCommand}


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
