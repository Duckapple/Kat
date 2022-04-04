from argparse import ArgumentParser
from commands.archive import archive
from commands.debug import debugCommand, choices as debugChoices
from commands.get import getCommand, getFlags, get
from commands.list import collectProblems, listFlags
from commands.read import readCommand
from commands.submit import submitCommand, Response, submitFlags
from commands.test import testCommand
from helpers.exceptions import InvalidProblemException
from helpers.types import problem

allowedSubmitOptions = ["archive", "force", "sound"]
allowedGetOptions = ["open"]

_HELP_TEXT = """\
You are in the REPL Kat work environment.

List of commands:
  exit      Quit from the work environment
  quit      Same as exit
  help      Show this message
  read      Read the current problem in your browser
  test      Test your current solution against files in test directory
  debug     Debug your solution, requires additional argument
  skip      Skip over the current problem
  submit    Submit the current problem
"""

def workCommand(data):
    print('Running the Kat work REPL. Run command "help" for more info.')
    if data["problem"] is not None:
        problems = [data["problem"]]
    else:
        problems = [x[0] for x in collectProblems(data)]
    currentIndex = 0
    previousProblem = None
    try:
        currentProblem = getProblem(currentIndex, data, problems)
    except InvalidProblemException:
        print("")
        print(f"Error: Specified problem does not exist")
        print("")
        return
    while True:
        if previousProblem != currentProblem:
            print('Problem:', currentProblem)
        previousProblem = currentProblem
        try:
            command = input('> ')
            if command == "exit" or command == "quit":
                break
            if command == "read":
                readCommand({'problem': [currentProblem], 'open': True})
            elif command == "test":
                testCommand({'problem': currentProblem})
            elif command.startswith("debug"):
                args = command.split()
                if len(args) == 1:
                    print("Please add additional debug subcommand. Either init, rte or wa")
                if args[1] not in debugChoices:
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
                    if currentProblem is None:
                        break
            elif command == "skip":
                archive(currentProblem)
                currentIndex += 1
                currentProblem = getProblem(currentIndex, data, problems)
                if currentProblem is None:
                    break
            elif command == "help":
                print(_HELP_TEXT)
            else:
                print('Unrecognized command. For help, write "help"')
        except KeyboardInterrupt:
            print('Shutdown by keyboard interrupt')
            return

def getProblem(currentIndex, data, problems):
    if currentIndex >= len(problems):
        print("No more problems to solve, well done.")
        return
    currentProblem = problems[currentIndex]

    data = {**data, 'problem': [currentProblem]}
    get(currentProblem, data)

    return currentProblem

def workParser(parsers: ArgumentParser):
    helpText = 'Initiate a loop of running a subset of Kat commands interactively, on a list of problems retrieved from the Kattis instance. Options given to this command will be applied to the relevant commands called in the environment.'
    parser = parsers.add_parser('work', help=helpText, description=helpText)
    parser.add_argument('-p', '--problem', help='Work on only 1 problem (this will ignore all list flags)', type=problem)
    getFlags(parser)
    submitFlags(parser)
    listFlags(parser)
