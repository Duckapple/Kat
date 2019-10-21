import os, subprocess
import re
from get import promptToGet

_LANGUAGE_GUESS = {
    '.c': 'C',
    '.c#': 'C#',
    '.c++': 'C++',
    '.cc': 'C++',
    '.cpp': 'C++',
    '.cs': 'C#',
    '.cxx': 'C++',
    '.go': 'Go',
    '.h': 'C++',
    '.hs': 'Haskell',
    '.java': 'Java',
    '.js': 'JavaScript',
    '.m': 'Objective-C',
    '.pas': 'Pascal',
    '.php': 'PHP',
    '.pl': 'Prolog',
    '.py': 'Python',
    '.rb': 'Ruby'
}

_LANGUAGE_COMMANDS = {
    '.py': ['python3', '@f'],
    '.php': ['php', '@f'],
    # TODO: Figure out how to possibly compile the class beforehand
    '.java': ['java', '@c'],
    # TODO: Support rest of the languages that kattis supports
}

_REQUIRES_CLASS = [
    '.java'
]

def test(args, options):
    problemName = args[0]
    
    if not os.path.exists(problemName):
        promptToGet(args, options)
        return

    # if programFile is not given, we will attempt to guess it
    programFile = args[1] if args[1:] else selectProgramFile(problemName)
    if(programFile == -1):
        return
    
    inFiles, ansFiles = getTestFiles(problemName)
    passed = True
    
    command = getCommand(problemName, programFile)
    directory = os.path.join(os.getcwd(), problemName)

    if(command == -1):
        return

    for inF, ansF in zip(inFiles, ansFiles):
        result = runSingleTest(command, directory, inF, ansF)
        if(not result):
            passed = False
        
    if passed and "-a" in options:
        archive(args, options)

def selectProgramFile(problemName):
    files = [formatProgramFile(problemName, f) for f in os.listdir(problemName)]
    files = list(filter(isValidProgramFile, files))
    
    if(len(files) == 0):
        print("No source file fould for problem '" + problemName + "'.\nCreate a file inside the folder matching the problem (for example '"+problemName+"/answer.py')")
        return -1
    
    if(len(files) > 1):
        print("Multiple source files found. Choose one:")
        i = 0
        for f in files:
            language = _LANGUAGE_GUESS[f['extension']]
            print(str(i+1)+") " + f['name'] + " ("+language+")")
            i+=1
        chosen = files[int(input("Enter number corresponding to a file: ")) - 1]
        print("Running tests on " + chosen['name'])
        return chosen
    
    return files[0]

def isValidProgramFile(file):
    return os.path.isfile(file["relativePath"]) and file["extension"] in _LANGUAGE_COMMANDS

def formatProgramFile(dir, file):
    return {
        "relativePath": os.path.join(dir, file),
        "extension": os.path.splitext(file)[1],
        "name": file,
    }

def getTestFiles(problemName):
    testPath = problemName + "/test"
    files = [f for f in os.listdir(testPath) if os.path.isfile(os.path.join(testPath, f))]
    inFiles = [testPath + "/" + f for f in files if f.endswith(".in")]
    ansFiles = [testPath + "/" + f for f in files if f.endswith(".ans")]

    return inFiles, ansFiles

def runSingleTest(command, directory, inFile, answerFile):
    inp = getBytesFromFile(inFile)
    answer = getBytesFromFile(answerFile).decode("utf-8")
    result = subprocess.run(command, stdout=subprocess.PIPE, input=inp, cwd=directory).stdout.decode("utf-8").replace("\r\n", "\n")

    if (answer == result):
        print("\U0001F49A", inFile, "succeeded")
        return True
    else:
        print("\U0000274C", inFile, "failed")
        print("expected:")
        print(answer)
        print("actual:")
        print(result)
        return False

def getCommand(problemName, programFile):
    if(programFile['extension'] not in _LANGUAGE_COMMANDS):
        print("Unsupported programming language")
        return -1

    cmd = _LANGUAGE_COMMANDS[programFile['extension']]

    className = "" if programFile['extension'] not in _REQUIRES_CLASS else detectClassName(problemName, programFile)
    if(className == -1):
        return -1
    return [p.replace("@f", programFile['name']).replace("@c", className) for p in cmd]
    
def detectClassName(dir, file):
    content = getBytesFromFile(file['relativePath']).decode("utf-8")
    match = re.search("class (\w+\\n)", content)
    if match is None:
        print("Could not detect class in file '"+file+"'")
        return -1
    
    return match.group(1).strip()

def getBytesFromFile(file):
    inFile = open(file, "rb")
    result = inFile.read()
    inFile.close()
    return result

