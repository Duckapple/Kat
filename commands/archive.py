from argparse import ArgumentParser
import os, shutil
from helpers.webutils import promptToFetch


def archiveCommand(data):
    for problem in data['problem']:
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
    parser.add_argument('problem', help='Name of problem to archive', nargs='+')
