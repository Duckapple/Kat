import os
from argparse import ArgumentParser
import shutil

from helpers.cli import yes
from helpers.fileutils import findProblemLocation
from helpers.types import problemList, folder
from helpers.webutils import promptToFetch

def unarchiveCommand(data):
    folder = None
    if data.get('target'):
        folder = data.get('target')
    if data.get("all"):
        folder = data.get('all')
        if folder is None:
            folder = ".archive/"
        print(f"You are about to unarchive all problems from {folder}. Are you sure you want to continue?")
        if not yes():
            return
        data["problem"] = [x for x in os.listdir(folder) if not x.startswith(".")]
    for problem in data['problem']:
        if folder is not None:
            if not folder.startswith("."):
                folder = "." + folder
            if not folder.endswith("/"):
                folder += "/"
        unarchive(problem, folder)

def unarchive(problemName, folder=None):
    if folder is None:
        folder = findProblemLocation(problemName)
    if folder is None:
        print("️️⚠️  You do not have this problem in your files")
        promptToFetch(problemName)
    if not folder:
        return
    try:
        shutil.move(folder + problemName, problemName)
        print(f"📦 Moved problem, {problemName}, to main folder from {folder}")
    except FileNotFoundError:
        print(f'Error: Problem "{problemName}" was not found in {folder}')

def unarchiveParser(parsers: ArgumentParser):
    helpText = 'Move problem from archive folder for active development.'
    parser = parsers.add_parser('unarchive', description=helpText, help=helpText)
    parser.add_argument('problem', help='Name of problem to unarchive', nargs='*', type=problemList)
    parser.add_argument('-t', '--target', help='This flag dentoes to archive the problem or problems into the specified folder', type=folder)
    parser.add_argument('-a', '--all', help='This flag denotes to unarchive all problems in the specified folder.', type=folder)
