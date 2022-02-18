import os
from argparse import ArgumentParser
import shutil

from helpers.cli import yes
from helpers.fileutils import findProblemLocation
from helpers.types import problemList
from helpers.webutils import promptToFetch

def unarchiveCommand(data):
    folder = None
    if data.get('temp'):
        folder = ".temp/"
    elif data.get('solved'):
        folder = '.solved/'
    if data.get("all"):
        if folder is None:
            folder = ".archive/"
        print(f"You are about to unarchive all problems from {folder}. Are you sure you want to continue?")
        if not yes():
            return
        data["problem"] = [x for x in os.listdir(folder) if not x.startswith(".")]
    for problem in data['problem']:
        unarchive(problem, folder)

def unarchive(problemName, folder):
    if folder is None:
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
    parser.add_argument('problem', help='Name of problem to unarchive', nargs='*', type=problemList)
    parser.add_argument('-a', '--all', help='This flag denotes to unarchive all problems in the specified folder.', action='store_true')
    parser.add_argument('-s', '--solved', help='This flag denotes to archive into the .solved folder', action='store_true')
    parser.add_argument('-t', '--temp', help='This flag denotes to archive into the temp folder', action='store_true')
