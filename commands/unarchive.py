from argparse import ArgumentParser
import shutil

from helpers.fileutils import findProblemLocation
from helpers.types import problemList
from helpers.webutils import promptToFetch

def unarchiveCommand(data):
    for problem in data['problem']:
        unarchive(problem)

def unarchive(problemName):
    folder = findProblemLocation(problemName)
    if folder is None:
        print("️️⚠️  You do not have this problem in your files")
        promptToFetch(problemName)
    if not folder:
        return
    shutil.move(folder + problemName, problemName)
    print("📦 Moved problem", problemName, "to main folder")

def unarchiveParser(parsers: ArgumentParser):
    helpText = 'Move problem from archive folder for active development.'
    parser = parsers.add_parser('unarchive', description=helpText, help=helpText)
    parser.add_argument('problem', help='Name of problem to unarchive', nargs='+', type=problemList)
