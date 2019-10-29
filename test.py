import os, subprocess

from programSelector import (
    selectProgramFile,
    formatProgramFile,
    getRunCommand,
    shouldCompile,
    compile,
)
from fileutils import getBytesFromFile
from get import promptToGet
from archive import archive


def test(args, options):
    problemName = args[0]
    directory = os.path.join(os.getcwd(), problemName)

    if not os.path.exists(problemName):
        promptToGet(args, options)
        return

    # if programFile is not given, we will attempt to guess it
    programFile = (
        formatProgramFile(args[1]) if args[1:] else selectProgramFile(problemName)
    )
    if programFile == -1:
        return

    print("🔎 Running tests on " + programFile["name"])

    if shouldCompile(programFile):
        if compile(programFile, directory) == -1:
            return

    inFiles, ansFiles = getTestFiles(problemName)
    passed = True

    command = getRunCommand(programFile)

    if command == -1:
        return

    for inF, ansF in zip(inFiles, ansFiles):
        result = runSingleTest(command, directory, inF, ansF)
        if not result:
            passed = False

    if passed and "-a" in options:
        archive(args, options)


def getTestFiles(problemName):
    testPath = problemName + "/test"
    files = [
        f for f in os.listdir(testPath) if os.path.isfile(os.path.join(testPath, f))
    ]
    inFiles = [testPath + "/" + f for f in files if f.endswith(".in")]
    ansFiles = [testPath + "/" + f for f in files if f.endswith(".ans")]

    # For some reason files aren't alwats given in the correct order, so we must sort the lists first
    inFiles.sort()
    ansFiles.sort()

    return inFiles, ansFiles


def runSingleTest(command, directory, inFile, answerFile):
    inp = getBytesFromFile(inFile)
    answer = getBytesFromFile(answerFile).decode("utf-8")
    result = (
        subprocess.run(command, stdout=subprocess.PIPE, input=inp, cwd=directory)
        .stdout.decode("utf-8")
        .replace("\r\n", "\n")
    )

    if answer == result:
        print("\U0001F49A", inFile, "succeeded")
        return True
    else:
        print("\U0000274C", inFile, "failed")
        print("expected:")
        print(answer)
        print("actual:")
        print(result)
        return False

testFlags = [
    ("archive", False),
    ("submit", False),
]