import os, subprocess

from helpers.programSelector import (
    selectProgramFile,
    formatProgramFile,
    getRunCommand,
    shouldCompile,
    compile,
)
from helpers.fileutils import getBytesFromFile
from helpers.webutils import promptToFetch
from commands.archive import archiveCommand


def testCommand(args, options):
    problemName = args[0]
    testIndice = args[1:] # gets test indexes for singulartests
    singularTest = len(testIndice) > 0 # bool for singulartests
    directory = os.path.join(os.getcwd(), problemName)

    # if it's a range of numbers (1-4) convert to list [1,2,3,4]
    # otherwise, convert to ints
    if singularTest:
        if not testIndice[0].isdigit():
            rangeIs = testIndice[0].split("-")
            testIndice = list(range(int(rangeIs[0]), int(rangeIs[1])+1))
        else:
            testIndice = [int(x) for x in testIndice]

    if not os.path.exists(problemName):
        promptToFetch(args, options)
        return

    # if programFile is not given, we will attempt to guess it
    programFile = selectProgramFile(problemName)
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

    for i, (inF, ansF) in enumerate(zip(inFiles, ansFiles)):
        if singularTest:
            if i+1 in testIndice:
                result = runSingleTest(command, directory, inF, ansF)
            else: 
                result = True
        else:
            result = runSingleTest(command, directory, inF, ansF)
        if not result:
            passed = False

    if passed and "archive" in options:
        archiveCommand(args, options)


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