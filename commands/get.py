import os

from commands.open import openCommand
from enum import Enum, auto

from commands.unarchive import unarchiveCommand
from helpers.webutils import fetchProblem


class GetResponse(Enum):
    Success = auto()
    Failure = auto()
    Redundant = auto()


def getCommand(problemName, options):
    if os.path.exists(problemName):
        return
    message = "👍 Successfully unarchived exercise", problemName + "!"
    if os.path.exists(".archive/" + problemName) or os.path.exists(".solved/" + problemName):
        unarchiveCommand(problemName, [])
    else:
        fetchProblem(problemName)
        message = "👍 Successfully initialized exercise", problemName + "!"

    print(message)
    if "open" in options:
        openCommand(problemName)


getFlags = [
    ("open", False),
]
