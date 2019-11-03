import os, shutil
from commands.get import promptToGet


def unarchiveCommand(args, options):
    if os.path.exists(args[0]):
        print("️️⚠️  You already have this problem in your main folder")
        return
    if not os.path.exists(".archive/" + args[0]):
        print("️️⚠️  This problem does not exist in .archive.")
        promptToGet(args, options)
        return
    shutil.move(".archive/" + args[0], args[0])
    print("📦 Moved problem", args[0], "from archive")
