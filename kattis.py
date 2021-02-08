#!/usr/bin/env python3
from commands.startup import startupCommand
from commands.work import workCommand
from commands.archive import archiveCommand
from commands.get import getCommand
from commands.submit import submitCommand
from commands.test import testCommand
from commands.watch import watchCommand
from commands.list import listCommand
from commands.read import readCommand
from helpers.exceptions import RedundantCommandException, InvalidProblemException
from commands.unarchive import unarchiveCommand
from commands.config import configCommand
from helpers.parser import parse

execCommand = {
    "archive":   archiveCommand,
    "config":    configCommand,
    "get":       getCommand,
    "list":      listCommand,
    "read":      readCommand,
    "startup":   startupCommand,
    "submit":    submitCommand,
    "test":      testCommand,
    "unarchive": unarchiveCommand,
    "watch":     watchCommand,
    "work":      workCommand,
}

def main():
    data = vars(parse())
    command = data["command"]

    if command in execCommand:
        try:
            execCommand[command](data)
        except (RedundantCommandException, InvalidProblemException) as error:
            print()
            print(error)
            print()

main()
