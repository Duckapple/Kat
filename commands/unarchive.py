import os, shutil
from helpers.webutils import promptToFetch

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
        promptToFetch(problemName, options)
        return
    shutil.move(folder + problemName, problemName)
    print("📦 Moved problem", problemName, "from " + solved[:-1])
