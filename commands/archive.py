from argparse import ArgumentParser
import os, shutil

from helpers.cli import yes
from helpers.types import problem, problemList, folder
from helpers.webutils import promptToFetch


def archiveCommand(data):
    folder = ".archive/"
    if data.get('target'):
        folder = data.get('target')
    if data.get("all"):
        folder = data.get("all")
        print(f"Warning: You are about to archive all problems in your current folder to {folder}. Do you want to continue?")
        if not yes():
            return
        data["problem"] = [x for x in os.listdir() if not x.startswith(".")]
    for problem in data['problem']:
        archive(problem, folder)

def archive(problemName, folder=".archive/"):
    if os.path.exists(folder + problemName):
        return
    if not os.path.exists(problemName):
        promptToFetch(problemName)
        return
    shutil.move(problemName, folder + problemName)
    print("📦 Moved problem", problemName, "to " + folder[:-1])

def archiveParser(parsers: ArgumentParser):
    helpText = 'Move problem to archive folder.'
    parser = parsers.add_parser('archive', description=helpText, help=helpText)
    parser.add_argument('problem', help='Name of problem to archive', nargs='*', type=problemList)
    parser.add_argument('-t', '--target', help='This flag dentoes to archive the problem or problems into the specified folder', type=folder)
    parser.add_argument('-a', '--all', help='This flag denotes to archive all problems in the current folder. This will not move any directories starting with "."', type=folder)
