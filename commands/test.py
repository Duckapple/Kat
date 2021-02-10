from argparse import ArgumentParser
from commands.submit import submitCommand
import os, re, subprocess

from helpers.programSelector import (
    selectProgramFile,
    formatProgramFile,
    getRunCommand,
    shouldCompile,
    compile,
)
from helpers.fileutils import getBytesFromFile
from helpers.webutils import promptToFetch
from commands.archive import archive


def testCommand(data):
    problemName = data['problem']
    directory = os.path.join(os.getcwd(), problemName)

    if not os.path.exists(problemName):
        promptToFetch(problemName)
        return

    # if programFile is not given, we will attempt to guess it
    programFile = (
        formatProgramFile(data["file"]) if "file" in data and data['file'] else selectProgramFile(problemName)
    )
    if not programFile:
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

    testsToRun = data['interval'] or None

    for i, (inF, ansF) in enumerate(zip(inFiles, ansFiles)):
        if testsToRun and i not in testsToRun:
            continue
        result = runSingleTest(command, directory, inF, ansF)
        if not result:
            passed = False

    shouldEnd = None

    if passed:
        if "submit" in data and data['submit']:
            submitCommand({"problem": problemName, "file": programFile['relativePath']})
            shouldEnd = True
        if "archive" in data and data['archive']:
            archive(problemName)
            shouldEnd = True
    if shouldEnd:
        return shouldEnd

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

def getInterval(inp):
    intervals = [intvl.strip() for intvl in inp.split(',')]
    result = []
    for interval in intervals:
        if re.match('\\d+-\\d+', interval):
            fromI, toI = [int(x.strip()) for x in interval.split('-')]
            result.extend(range(fromI - 1, toI))
        else:
            result.append(int(interval.strip()) - 1)
    return result

def testParser(parsers: ArgumentParser):
    helpText = 'Test a problem against the problem test cases.'
    parser = parsers.add_parser('test', description=helpText, help=helpText)
    testFlags(parser)

def testFlags(parser):
    parser.add_argument('problem', help='The problem to test.')
    parser.add_argument('file', nargs='?', help='Name of the specific file to test')
    parser.add_argument('-i', '--interval', help='Determine an interval of tests to run, instead of all tests. Examples are "1", "1-3", "1,3-5".', type=getInterval)
    parser.add_argument('-a', '--archive', action='store_true', help='Archive the problem if all tests succeed.')
    parser.add_argument('-s', '--submit', action='store_true', help='Submit the problem if all tests succeed.')
