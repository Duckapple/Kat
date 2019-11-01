import os, shutil
from commands.get import promptToGet


def archive(args, options):
    if os.path.exists(".archive/" + args[0]):
        print("️️⚠️  You have already archived this problem.")
        return
    if not os.path.exists(args[0]):
        promptToGet(args, options)
        return
    shutil.move(args[0], ".archive/" + args[0])
    print("📦 Moved problem", args[0], "to archive")
