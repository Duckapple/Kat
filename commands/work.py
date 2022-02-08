from argparse import ArgumentParser
from commands.archive import archive
from commands.debug import debugCommand
import commands.debug
from commands.get import getCommand, getFlags
from commands.list import collectProblems, listFlags
from commands.read import readCommand
from commands.submit import submitCommand, Response, submitFlags
from commands.test import testCommand

allowedSubmitOptions = ["archive", "force", "sound"]
allowedGetOptions = ["open"]

_HELP_TEXT = """\
You are in the REPL Kat work environment.
a list of problems to 

List of commands:
  exit      Quit from the work environment
  help      Show this message
  read      Read the current problem in your browser
  test      Test your current solution against files in test directory
  debug     Debug your solution, requires additional argument
  skip      Skip over the current problem
  submit    Submit the current problem
"""

def workCommand(data):
    print('Running the Kat work REPL. Run command "help" for more info.')
    problems = [x[0] for x in collectProblems(data)]
    currentIndex = 0
    previousProblem = None
    currentProblem = getProblem(currentIndex, data, problems)
    while True:
        if previousProblem != currentProblem:
            print('Problem:', currentProblem)
        previousProblem = currentProblem
        try:
            command = input('> ')
            if command == "exit":
                break
            if command == "read":
                readCommand({'problem': [currentProblem], 'open': True})
            elif command == "test":
                testCommand({'problem': currentProblem})
            elif command.startswith("debug"):
                args = command.split()
                if len(args) == 1:
                    print("Please add additional debug subcommand. Either init, rte or wa")
                if args[1] not in commands.debug.choices:
                    print("Invalid subcommand for debug")
                else:
                    debugdata = {'problem': currentProblem, 'subcommand': args[1], 'iterations': None}
                    if len(args) == 3:
                        debugdata['iterations'] = int(args[2])
                    debugCommand(debugdata)


            elif command == "submit":
                response = submitCommand({**data, 'problem': currentProblem})

                if response == Response.Success:
                    currentIndex += 1
                    currentProblem = getProblem(currentIndex, data, problems)
            elif command == "skip":
                archive(currentProblem)
                currentIndex += 1
                currentProblem = getProblem(currentIndex, data, problems)
            elif command == "help":
                print(_HELP_TEXT)
        except KeyboardInterrupt:
            print('Shutdown by keyboard interrupt')
            return

def getProblem(currentIndex, data, problems):
    currentProblem = problems[currentIndex]

    getCommand({**data, 'problem': [currentProblem]})

    return currentProblem

def workParser(parsers: ArgumentParser):
    helpText = 'Initiate a loop of running a subset of Kat commands interactively, on a list of problems retrieved from the Kattis instance. Options given to this command will be applied to the relevant commands called in the environment.'
    parser = parsers.add_parser('work', help=helpText, description=helpText)
    getFlags(parser)
    submitFlags(parser)
    listFlags(parser)
