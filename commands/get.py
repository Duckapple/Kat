from argparse import ArgumentParser
import subprocess

from helpers.types import problem, problemList
from helpers.programSelector import formatCommand, selectProgramFile
from helpers.config import getConfig
from commands.web import webCommand
from commands.unarchive import unarchive
from helpers.exceptions import InvalidProblemException
from helpers.fileutils import findProblemLocation
from helpers.webutils import fetchProblem


def getCommand(data):
    print(data)
    solved = []
    for problem in data['problem']:
        try:
            folder = get(problem, data)
            if folder == ".solved/":
                solved.append(problem)
        except InvalidProblemException:
            print("")
            print(f"Error: Problem '{problem}' does not exist")
            print("")
    return solved

def get(problemName: str, data: dict):
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
    else:
        print("👍 You already have " + problemName)

    if "open" in data and data['open']:
        webCommand(problemName)

    fileOpener = getConfig().get('kat', {}).get('openfilecommand')
    if fileOpener:
        file = selectProgramFile(problemName)
        subprocess.run(formatCommand(fileOpener, file).split())
    return folder

def getParser(parsers: ArgumentParser):
    helpText = 'Get a problem and its tests from the Kattis instance.'
    parser = parsers.add_parser('get', help=helpText, description=helpText)
    parser.add_argument('problem', help='Name of problem to get', nargs='+', type=problemList)
    getFlags(parser)

def getFlags(parser):
    parser.add_argument('-o', '--open', action='store_true', help='Open the problem in your web-browser.')
    parser.add_argument('-l', '--language', type=str, help='Choose the language to initialize the problem in')
