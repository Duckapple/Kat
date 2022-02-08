import filecmp
import os
import shutil
from argparse import ArgumentParser
import subprocess
from commands.unarchive import unarchive
from helpers.fileutils import findProblemLocation
from helpers.programSelector import getAndPrepareRunCommand, selectProgramFile
from helpers.webutils import fetchProblem


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
    generator = "debug/generator.py"
    testIn = "debug/test.in"

    solutionCommand = getSolutionCommand(problemName)
    if not solutionCommand:
        print('Could not find solution file')
        return

    os.chdir(os.path.join(os.curdir, problemName))

    try:
        print(f"Running {iterations} iterations")
        for i in range(1, iterations + 1):
            print(i)
            with open(testIn, 'w') as testInFile:
                subprocess.run(['python', generator], stdout=testInFile)
            with open(testIn, 'r') as testInFile:
                res = subprocess.run(solutionCommand, stdin=testInFile, stdout=subprocess.DEVNULL)
                if res.returncode != 0:
                    print("Error found")
                    break
    except KeyboardInterrupt:
        print('Interrupted.')
    finally:
        os.chdir('..')

def WACommand(problemName, iterations):
    generator = "debug/generator.py"
    bruteForce = "debug/bruteforce.py"
    testIn = "debug/test.in"
    solutionOut = "debug/WA.ans"
    bruteOut = "debug/test.ans"

    solutionCommand = getSolutionCommand(problemName)
    if not solutionCommand:
        print('Could not find solution file')
        return

    os.chdir(os.path.join(os.curdir, problemName))

    try:
        print(f"Running {iterations} iterations")
        for i in range(1, iterations + 1):
            print(i)
            with open(testIn, 'w') as testInFile:
                subprocess.run(['python', generator], stdout=testInFile)
            with open(testIn, 'r') as testInFile:
                with open(solutionOut, 'w') as solutionOutFile:
                    subprocess.run(solutionCommand, stdin=testInFile, stdout=solutionOutFile)
            with open(testIn, 'r') as testInFile:
                with open(bruteOut, 'w') as bruteOutFile:
                    subprocess.run(['python', bruteForce], stdin=testInFile, stdout=bruteOutFile)

            if not filecmp.cmp(solutionOut, bruteOut):
                print("Error found: Output doesn't match")
                break
    except KeyboardInterrupt:
        print('Interrupted.')
    finally:
        os.chdir('..')


def getSolutionCommand(problemName):
    programFile = selectProgramFile(problemName)
    return getAndPrepareRunCommand(programFile)

choices = [
    'init', 'rte', 'wa'
]

def debugParser(parsers: ArgumentParser):
    helpText = 'Use on of several functions to help debug a solution.'
    parser = parsers.add_parser('debug', help=helpText, description=helpText)
    parser.add_argument('problem', help='Name of problem to debug')
    parser.add_argument('subcommand', help='Name of subcommand you want to run', choices=choices)
    parser.add_argument('iterations', help='Number of iterations that RTEValidator and WAValidator should run.', nargs='?', type=int)
