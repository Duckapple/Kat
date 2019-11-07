import os, shutil
from commands.get import promptToGet
from helpers.exceptions import RedundantCommandException


def unarchiveCommand(problemName, options):
    if os.path.exists(problemName):
        raise RedundantCommandException("️️⚠️  You already have this problem in your main folder")
    if not os.path.exists(".archive/" + problemName):
        print("️️⚠️  This problem does not exist in .archive.")
        promptToGet(problemName, options)
        return
    shutil.move(".archive/" + problemName, problemName)
    print("📦 Moved problem", problemName, "from archive")
