from argparse import ArgumentParser
import subprocess
from helpers.programSelector import formatCommand, selectProgramFile
from helpers.config import getConfig
from commands.web import webCommand
from commands.unarchive import unarchive
from helpers.exceptions import InvalidProblemException
from helpers.fileutils import findProblemLocation
from helpers.webutils import fetchProblem


def debugCommand(data):
choices = [
    'init', 'RTE', 'WA'
]

def getParser(parsers: ArgumentParser):
    helpText = 'Use on of several functions to help debug a solution.'
    parser = parsers.add_parser('debug', help=helpText, description=helpText)
    parser.add_argument('problem', help='Name of problem to debug', nargs='+')
    parser.add_argument('subcommand', help='Name of subcommand you want to run', nargs='+')
    getFlags(parser)

def getFlags(parser):
    #parser.add_argument('-o', '--open', action='store_true', help='Open the problem in your web-browser.')
    #parser.add_argument('-l', '--language', type=str, help='Choose the language to initialize the problem in')
