import os, re, subprocess

from helpers.fileutils import getBytesFromFile
from helpers.config import getConfig

# import os, subprocess, re

cfg = getConfig()

_LANGUAGE_GUESS = cfg["File associations"]

_LANGUAGE_RUN_COMMANDS = cfg["Run commands"]

_LANGUAGE_COMPILE_COMMANDS = cfg["Compile commands"]


def selectProgramFile(problemName):
    # Get all files, and format them
    files = [
        formatProgramFile(os.path.join(problemName, f)) for f in os.listdir(problemName)
    ]
    # ..but only select those which we support
    files = list(filter(isValidProgramFile, files))

    if len(files) == 0:
        print(
            "No source file fould for problem '"
            + problemName
            + "'.\nCreate a file inside the folder matching the problem (for example '"
            + problemName
            + "/answer.py')"
        )
        return -1

    if len(files) == 1:
        return files[0]

    print("Multiple source files found. Choose one:")
    i = 0
    for f in files:
        language = guessLanguage(f)
        print(str(i + 1) + ") " + f["name"] + " (" + language + ")")
        i += 1
    chosen = files[int(input("Enter number corresponding to a file: ")) - 1]
    return chosen


def isValidProgramFile(file):
    return (
        os.path.isfile(file["relativePath"])
        and str(guessLanguage(file)) in _LANGUAGE_RUN_COMMANDS
    )


def formatProgramFile(file):
    return {
        "relativePath": file,
        "extension": os.path.splitext(file)[1],
        "name": os.path.basename(file),
    }


def detectClassName(file):
    content = getBytesFromFile(file["relativePath"]).decode("utf-8")
    match = re.search("class (\\w+)", content)
    if match is None:
        print("Could not detect class in file '" + file["name"] + "'")
        return -1

    return match.group(1).strip()


def getRunCommand(programFile):
    if guessLanguage(programFile) not in _LANGUAGE_RUN_COMMANDS:
        print("Unsupported programming language")
        return -1

    cmd = _LANGUAGE_RUN_COMMANDS.getcommand(guessLanguage(programFile))

    return [formatCommand(p, programFile) for p in cmd]


def formatCommand(cmd, file):
    className = "" if not requiresClass(file) else detectClassName(file)
    if className == -1:
        return -1

    cmd = cmd.replace("@p", file["name"][:-(len(file["extension"]))])
    cmd = cmd.replace("@f", file["name"])
    cmd = cmd.replace("@c", className)
    cmd = cmd.replace("@d", file["relativePath"].replace("\\" + file["name"], ""))
    
    return cmd


def compile(file, directory):
    if guessLanguage(file) not in _LANGUAGE_COMPILE_COMMANDS:
        print("Files of this type should not be compiled")
        return -1
    print("Compiling " + file["name"])

    cmd = [
        formatCommand(p, file) for p in _LANGUAGE_COMPILE_COMMANDS.getcommand(guessLanguage(file))
    ]
    if -1 in cmd:
        print("Error duing compilation")
        return -1

    compileResult = subprocess.run(cmd, cwd=directory)
    if compileResult.returncode != 0:
        print('Compilation failed.')
        return -1


def shouldCompile(file):
    return guessLanguage(file) in _LANGUAGE_COMPILE_COMMANDS


def guessLanguage(file):
    return (
        _LANGUAGE_GUESS[file["extension"]]
        if file["extension"] in _LANGUAGE_GUESS
        else -1
    )


def requiresClass(file):
    return guessLanguage(file) == "Java"
