import shutil

from helpers.fileutils import findProblemLocation
from helpers.webutils import promptToFetch


def unarchiveCommand(problemName, options):
    folder = findProblemLocation(problemName)
    if folder is None:
        print("️️⚠️  You do not have this problem in your files")
        promptToFetch(problemName, options)
    if folder == "":
        return
    shutil.move(folder + problemName, problemName)
    print("📦 Moved problem", problemName, "to main folder")


