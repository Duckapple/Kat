import os
import re
import subprocess
from helpers.fileutils import getBytesFromFile
from helpers.config import getConfig, toCommandArray

cfg = getConfig()

_LANGUAGE_GUESS = cfg.get("File associations", {})

_LANGUAGE_RUN_COMMANDS = cfg.get("Run commands", {})

_LANGUAGE_COMPILE_COMMANDS = cfg.get("Compile commands", {})


def getAndPrepareRunCommand(programFile):
    directory = os.path.dirname(programFile['relativePath'])
    if shouldCompile(programFile):
        if compile(programFile, directory) == None:
            return
    return getRunCommand(programFile)


def selectProgramFile(problemName):
    # Get all files, and format them
    files = [
        formatProgramFile(os.path.join(problemName, f)) for f in os.listdir(problemName)
    ]
    # If we have a 'src' directory, scan that too
    for f in files:
        if f['name'] == 'src' and f['extension'] == '':
            files.extend([
                formatProgramFile(os.path.join(f['relativePath'], f2)) for f2 in os.listdir(f['relativePath'])
            ])
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
        return None

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
        and str(guessLanguage(file)).lower() in _LANGUAGE_RUN_COMMANDS
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
        return ""

    return match.group(1).strip()


def getRunCommand(programFile):
    if guessLanguage(programFile) not in _LANGUAGE_RUN_COMMANDS:
        print("Unsupported programming language")
        return None

    cmd = toCommandArray(_LANGUAGE_RUN_COMMANDS.get(
        guessLanguage(programFile)))

    formattedCommand = [formatCommand(p, programFile) for p in cmd]
    if None in formattedCommand:
        return None
    return formattedCommand


def formatCommand(cmd, file):
    className = "" if not requiresClass(file) else detectClassName(file)
    if className == None:
        return None

    cmd = cmd.replace("@p", file["name"][:-(len(file["extension"]))])
    cmd = cmd.replace("@f", file["name"])
    cmd = cmd.replace("@c", className)
    cmd = cmd.replace("@d", os.path.split(file["relativePath"])[0])
    cmd = cmd.replace("@s", file["relativePath"])
    return cmd


def compile(file, directory):
    if guessLanguage(file) not in _LANGUAGE_COMPILE_COMMANDS:
        print("Files of this type should not be compiled")
        return None
    print("Compiling " + file["name"])

    cmd = [
        formatCommand(p, file) for p in toCommandArray(_LANGUAGE_COMPILE_COMMANDS.get(guessLanguage(file)))
    ]
    if None in cmd:
        print("Error duing compilation")
        return None

    compileResult = subprocess.run(cmd, cwd=directory)
    if compileResult.returncode != 0:
        print('Compilation failed.')
        return None

    return True


def shouldCompile(file):
    return guessLanguage(file) in _LANGUAGE_COMPILE_COMMANDS


def guessLanguage(file):
    return (
        _LANGUAGE_GUESS[file["extension"]].lower()
        if file["extension"] in _LANGUAGE_GUESS
        else None
    )


def requiresClass(file):
    return guessLanguage(file) == "java"
