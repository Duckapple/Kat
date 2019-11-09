import os
import shutil


def getBytesFromFile(file):
    inFile = open(file, "rb")
    result = inFile.read()
    inFile.close()
    return result


def createBoilerplate(problemName):
    shutil.copy2(
        os.path.dirname(os.path.realpath(__file__)) + "/../boilerplate/boilerplate.py",
        problemName + "/" + problemName + ".py",
    )


def findProblemLocation(problemName):
    folders = [".archive/", ".solved/", ""]
    for folder in folders:
        if os.path.exists(folder + problemName):
            return folder
    return None