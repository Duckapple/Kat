import os, shutil
from commands.get import promptToGet


def unarchiveCommand(arg, options):
    problemName = arg
    if os.path.exists(problemName):
        print("️️⚠️  You already have this problem in your main folder")
        return
    if not os.path.exists(".archive/" + problemName):
        print("️️⚠️  This problem does not exist in .archive.")
        promptToGet(arg, options)
        return
    shutil.move(".archive/" + problemName, problemName)
    print("📦 Moved problem", problemName, "from archive")
