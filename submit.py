import subprocess, os
from archive import archive

def submit(args, options):
    rootDir = os.path.dirname(os.path.realpath(__file__))
    libPath = os.path.join(rootDir, "lib_submit.py")
    programPath = os.path.join(os.getcwd(), args[0], args[0] + ".py")
    command = ["python3", libPath, "-p", args[0], programPath]
    if "-f" in options:
        command.append("-f")
    subprocess.run(args=command)
    if "-a" in options:
        archive(args, options)