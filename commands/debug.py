import filecmp
import os
import shutil
from argparse import ArgumentParser
import subprocess
from helpers.programSelector import formatCommand, selectProgramFile
from helpers.config import getConfig
from commands.web import webCommand
from commands.unarchive import unarchive
from helpers.exceptions import InvalidProblemException
from helpers.fileutils import findProblemLocation
from helpers.webutils import fetchProblem, promptToFetch





def debugCommand(data):
    problemName = data['problem']
    subcommand = data["subcommand"]
    iterations = data["iterations"] if data["iterations"] else 1000

    message = ""
    folder = findProblemLocation(problemName)
    if folder is None:
        overrideLanguage = data['language']
        fetchProblem(problemName, overrideLanguage)
        message = "👍 Successfully initialized exercise " + problemName + "!"

    elif folder != "":
        unarchive(problemName)
        message = "👍 Successfully unarchived exercise " + problemName + "!"
    if message != "":
        print(message)

    if subcommand == "init":
        initCommand(problemName)

    elif subcommand == "rte":
        RTECommand(problemName, iterations)

    elif subcommand == "wa":
        WACommand(problemName, iterations)



def initCommand(problemName):
    original = os.path.dirname(os.path.realpath(__file__)) + "/../resources/debug"
    shutil.copytree(original, problemName + "/debug", dirs_exist_ok=True)
    print("👍 Initialized debug folder")

def RTECommand(problemName, iterations):
    print("getting here")
    generator = f"{problemName}/debug/generator.py"
    solution = f"{problemName}/{problemName}.py"
    testIn = f"{problemName}/debug/test.in"
    solutionOut = f"{problemName}/debug/RTE.ans"

    print(f"Running {iterations} iterations")
    for i in range(1, iterations + 1):
        print(i)
        os.system(f"python {generator} > {testIn}")
        code = os.system(f"python {solution} < {testIn} > {solutionOut}")
        if code != 0:
            print("Error found")
            break

def WACommand(problemName, iterations):
    generator = f"{problemName}/debug/generator.py"
    solution = f"{problemName}/{problemName}.py"
    bruteForce = f"{problemName}/debug/bruteforce.py"
    testIn = f"{problemName}/debug/test.in"
    solutionOut = f"{problemName}/debug/WA.ans"
    bruteOut = f"{problemName}/debug/test.ans"


    print(f"Running {iterations} iterations")
    for i in range(1, iterations + 1):
        print(i)
        os.system(f"python {generator} > {testIn}")
        os.system(f"python {solution} < {testIn} > {solutionOut}")
        os.system(f"python {bruteForce} < {testIn} > {bruteOut}")
        if not filecmp.cmp(solutionOut, bruteOut):
            print("Error found")
            break




choices = [
    'init', 'rte', 'wa'
]

def debugParser(parsers: ArgumentParser):
    helpText = 'Use on of several functions to help debug a solution.'
    parser = parsers.add_parser('debug', help=helpText, description=helpText)
    parser.add_argument('problem', help='Name of problem to debug')
    parser.add_argument('subcommand', help='Name of subcommand you want to run', choices=choices)
    parser.add_argument('iterations', help='Number of iterations that RTEValidator and WAValidator should run.', nargs='?', type=int)


def debugFlags(parser):
    pass
    #parser.add_argument('-o', '--open', action='store_true', help='Open the problem in your web-browser.')
    #parser.add_argument('-l', '--language', type=str, help='Choose the language to initialize the problem in')
