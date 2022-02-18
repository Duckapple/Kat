from argparse import ArgumentParser
import os, shutil

from helpers.types import problem, problemList
from helpers.webutils import promptToFetch


def archiveCommand(data):
    if data.get("all"):
        data["problem"] = [x for x in os.listdir() if not x.startswith(".")]
    for problem in data['problem']:
        if data.get("solved"):
            archive(problem, ".solved/")
        elif data.get("temp"):
            archive(problem, ".temp/")
        else:
            archive(problem)

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
    parser.add_argument('-s', '--solved', help='This flag denotes to archive into the .solved folder', action='store_true')
    parser.add_argument('-a', '--all', help='This flag denotes to archive all problems in the current folder. This will not move any directories starting with "."', action='store_true')
    parser.add_argument('-t', '--temp', help='This flag denotes to archive into the temp folder', action='store_true')
