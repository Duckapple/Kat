from commands.archive import archiveCommand
from commands.get import getCommand, GetResponse
from commands.list import collectProblems
from commands.read import readCommand
from commands.submit import submitCommand
from commands.test import testCommand
from commands.unarchive import unarchiveCommand

allowedSubmitOptions = ["archive", "force", "sound"]
allowedGetOptions = ["open"]


def workCommand(args, options):
    problems = [x[0] for x in collectProblems(args, [])]
    currentI = 0
    currentProblem = getProblem(currentI, options, problems)
    while True:
        command = input()
        if command == "exit":
            break
        if command == "read":
            readCommand([currentProblem], ["-o"])
        elif command == "test":
            testCommand([currentProblem], [])
        elif command == "submit":
            submitOptions = [x for x in allowedSubmitOptions if x in options]
            successful = False
            try:
                successful = submitCommand([currentProblem], submitOptions)
            except:
                pass

            if successful:
                currentI += 1
                currentProblem = getProblem(currentI, options, problems)
        elif command == "skip":
            archiveCommand([currentProblem], [])
            currentI += 1
            currentProblem = getProblem(currentI, options, problems)


def getProblem(currentI, options, problems):
    currentProblem = problems[currentI]
    getOptions = [x for x in allowedGetOptions if x in options]
    try:
        getCommand([currentProblem], getOptions)
    except:
        unarchiveCommand([currentProblem], [])

    return currentProblem
