import os, shutil
from commands.get import promptToGet
from helpers.exceptions import RedundantCommandException
archive = ".archive/"
solved = ".solved/"


def unarchiveCommand(problemName, options):
    if os.path.exists(problemName):
        return
    folder = ""
    if os.path.exists(archive + problemName):
        folder = archive
    elif os.path.exists(solved + problemName):
        folder = solved
    else:
        print("️️⚠️  This problem does not exist in .archive.")
        promptToGet(problemName, options)
        return
    shutil.move(folder + problemName, problemName)
    print("📦 Moved problem", problemName, "from " + solved[:-1])
