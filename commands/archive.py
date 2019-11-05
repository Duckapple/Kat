import os, shutil
from commands.get import promptToGet
from helpers.exceptions import RedundantCommandException


def archiveCommand(args, options, folder=".archive/"):

    if os.path.exists(folder + args[0]):
        raise RedundantCommandException("️️⚠️  You have already archived this problem.")
    if not os.path.exists(args[0]):
        promptToGet(args, options)
        return
    shutil.move(args[0], folder + args[0])
    print("📦 Moved problem", args[0], "to archive")
