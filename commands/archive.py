import os, shutil
from commands.get import promptToGet
from helpers.exceptions import RedundantCommandException


def archiveCommand(problemName, options, folder=".archive/"):
    if os.path.exists(folder + problemName):
        raise RedundantCommandException("️️⚠️  You have already archived this problem.")
    if not os.path.exists(problemName):
        promptToGet(problemName, options)
        return
    shutil.move(problemName, folder + problemName)
    print("📦 Moved problem", problemName, "to archive")
