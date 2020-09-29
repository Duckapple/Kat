from commands.archive import archiveCommand
from commands.get import getCommand
from commands.list import collectProblems
from commands.read import readCommand
from commands.submit import submitCommand, Response
from commands.test import testCommand
from helpers.exceptions import RedundantCommandException, InvalidProblemException

allowedSubmitOptions = ["archive", "force", "sound"]
allowedGetOptions = ["open"]


def workCommand(args, options):
    problems = [x[0] for x in collectProblems(args, [])]
    currentI = 0
    currentProblem = getProblem(currentI, options, problems)
    while True:
        try:
            command = input()
            if command == "exit":
                break
            if command == "read":
                readCommand(currentProblem, ["-o"])
            elif command == "test":
                testCommand([currentProblem], [])
            elif command == "submit":
                submitOptions = [x for x in allowedSubmitOptions if x in options]
                successful = False
                try:
                    successful = submitCommand([currentProblem], submitOptions)
                except Exception as error:
                    print(error)

                if successful == Response.Success:
                    currentI += 1
                    currentProblem = getProblem(currentI, options, problems)
            elif command == "skip":
                archiveCommand(currentProblem, [])
                currentI += 1
                currentProblem = getProblem(currentI, options, problems)
        except (InvalidProblemException, RedundantCommandException) as error:
            print()
            print(error)
            print()


def getProblem(currentI, options, problems):
    currentProblem = problems[currentI]
    getOptions = [x for x in allowedGetOptions if x in options]

    getCommand(currentProblem, getOptions)

    return currentProblem
