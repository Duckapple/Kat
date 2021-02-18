#!/usr/bin/env python3
import traceback
from commands.contest import contestCommand
from helpers.webutils import submitError
from helpers.cli import yes
from commands.startup import startupCommand
from commands.work import workCommand
from commands.archive import archiveCommand
from commands.get import getCommand
from commands.submit import submitCommand
from commands.test import testCommand
from commands.watch import watchCommand
from commands.list import listCommand
from commands.read import readCommand
from commands.unarchive import unarchiveCommand
from commands.config import configCommand
from helpers.parser import parse

execCommand = {
    "archive":   archiveCommand,
    "config":    configCommand,
    "contest":   contestCommand,
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
    try:
        data = vars(parse())
        command = data.get("command")

        if command in execCommand:
            execCommand[command](data)
    except (Exception) as error:
        print()
        print(*traceback.format_exception(None, error, error.__traceback__))
        print(f"Error occurred:\n {error}\n")
        print("The program ran into a problem while running, do you want to create an issue on github?")
        if yes():
            submitError(error)

main()
