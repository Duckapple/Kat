#!/usr/bin/env python3
import sys, os, shutil, subprocess

from archive import archive
from get import get
from submit import submit
from test import test
from help import printHelp, helpIfNotCommand

def divideArgs(args):
    arg = []
    options = []
    for word in args:
        if ("-" in word):
            options.append(word)
        else:
            arg.append(word)
    return arg, options

execCommand = {
    "archive": archive,
    "get": get,
    "submit": submit,
    "test": test
}

def main():
    args, options = divideArgs(sys.argv)
    helpy = "-h" in options
    command = args[1]
    args = args[2:]

    if (helpy):
        printHelp(command)
    else: 
        execCommand.get(command, helpIfNotCommand(command))(args, options)
    
main()