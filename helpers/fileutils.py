import shutil

from os import listdir, getcwd
from os.path import isfile, join, dirname, realpath, exists


def getBytesFromFile(file):
    inFile = open(file, "rb")
    result = inFile.read()
    inFile.close()
    return result


def createBoilerplate(problemName):
    shutil.copy2(
        dirname(realpath(__file__)) + "/../boilerplate/boilerplate.py",
        problemName + "/" + problemName + ".py",
    )

def getAllProblems():
    blacklist = [".archive", ".solved", ".git", '__pycache__']
    path = getcwd()
    folders = [f for f in listdir(path) if not isfile(join(path, f)) and not f in blacklist]

    return folders

def findProblemLocation(problemName):
    folders = [".archive/", ".solved/", ""]
    for folder in folders:
        if exists(folder + problemName):
            return folder
    return None
