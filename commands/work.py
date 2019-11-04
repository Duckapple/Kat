from commands.archive import archive
from commands.get import get
from commands.list import collectProblems
from commands.submit import submit
from commands.test import test
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
        elif command == "test":
            test([currentProblem], [])
        elif command == "submit":
            submitOptions = [x for x in allowedSubmitOptions if x in options]
            successful = submit([currentProblem], submitOptions)
            if successful:
                currentI += 1
                currentProblem = getProblem(currentI, options, problems)
        elif command == "skip":
            archive([currentProblem], [])
            currentI += 1
            currentProblem = getProblem(currentI, options, problems)


def getProblem(currentI, options, problems):
    currentProblem = problems[currentI]
    getOptions = [x for x in allowedGetOptions if x in options]
    get([currentProblem], getOptions)
    return currentProblem
