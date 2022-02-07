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
        initCommand()


def initCommand():
    original = os.path.dirname(os.path.realpath(__file__)) + "/../resources/debug"
    shutil.copytree(original, "debug")


choices = [
    'init', 'RTE', 'WA'
]

def debugParser(parsers: ArgumentParser):
    helpText = 'Use on of several functions to help debug a solution.'
    parser = parsers.add_parser('debug', help=helpText, description=helpText)
    parser.add_argument('problem', help='Name of problem to debug')
    parser.add_argument('subcommand', help='Name of subcommand you want to run', choices=choices)


def debugFlags(parser):
    pass
    #parser.add_argument('-o', '--open', action='store_true', help='Open the problem in your web-browser.')
    #parser.add_argument('-l', '--language', type=str, help='Choose the language to initialize the problem in')
