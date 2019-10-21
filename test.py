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

_LANGUAGE_RUN_COMMANDS = {
    '.py': ['python3', '@f'],
    '.php': ['php', '@f'],
    '.java': ['java', '@c'],
    # TODO: Support rest of the languages that kattis supports
}

_LANGUAGE_COMPILE_COMMANDS = {
    '.java': ['javac', '@f']
}

_LANGUAGE_REQUIRES_CLASS = [
    '.java'
]

def test(args, options):
    problemName = args[0]
    directory = os.path.join(os.getcwd(), problemName)
    
    if not os.path.exists(problemName):
        promptToGet(args, options)
        return

    # if programFile is not given, we will attempt to guess it
    programFile = formatProgramFile(args[1]) if args[1:] else selectProgramFile(problemName)
    if(programFile == -1):
        return
    
    if(shouldCompile(programFile)):
        if(compile(programFile, directory) == -1):
            return
    
    inFiles, ansFiles = getTestFiles(problemName)
    passed = True
    
    command = getRunCommand(programFile)

    if(command == -1):
        return

    for inF, ansF in zip(inFiles, ansFiles):
        result = runSingleTest(command, directory, inF, ansF)
        if(not result):
            passed = False
        
    if passed and "-a" in options:
        archive(args, options)

def selectProgramFile(problemName):
    # Get all files, and format them
    files = [formatProgramFile(os.path.join(problemName, f)) for f in os.listdir(problemName)]
    # ..but only select those which we support
    files = list(filter(isValidProgramFile, files))
    
    if(len(files) == 0):
        print("No source file fould for problem '" + problemName + "'.\nCreate a file inside the folder matching the problem (for example '"+problemName+"/answer.py')")
        return -1
    
    if(len(files) == 1):
        return files[0]
    
    print("Multiple source files found. Choose one:")
    i = 0
    for f in files:
        language = _LANGUAGE_GUESS[f['extension']]
        print(str(i+1)+") " + f['name'] + " ("+language+")")
        i+=1
    chosen = files[int(input("Enter number corresponding to a file: ")) - 1]
    print("Running tests on " + chosen['name'])
    return chosen

def isValidProgramFile(file):
    return os.path.isfile(file["relativePath"]) and file["extension"] in _LANGUAGE_RUN_COMMANDS

def formatProgramFile(file):
    return {
        "relativePath": file,
        "extension": os.path.splitext(file)[1],
        "name": os.path.basename(file),
    }

def getTestFiles(problemName):
    testPath = problemName + "/test"
    files = [f for f in os.listdir(testPath) if os.path.isfile(os.path.join(testPath, f))]
    inFiles = [testPath + "/" + f for f in files if f.endswith(".in")]
    ansFiles = [testPath + "/" + f for f in files if f.endswith(".ans")]

    # For some reason the files are loaded in descending order, so we need to reverse the lists
    inFiles.reverse()
    ansFiles.reverse()

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

def getRunCommand(programFile):
    if(programFile['extension'] not in _LANGUAGE_RUN_COMMANDS):
        print("Unsupported programming language")
        return -1

    cmd = _LANGUAGE_RUN_COMMANDS[programFile['extension']]

    return [formatCommand(p, programFile) for p in cmd]
    
def formatCommand(cmd, file):
    className = "" if file['extension'] not in _LANGUAGE_REQUIRES_CLASS else detectClassName(file)
    if(className == -1):
        return -1

    return cmd.replace("@f", file['name']).replace("@c", className)

def detectClassName(file):
    content = getBytesFromFile(file['relativePath']).decode("utf-8")
    match = re.search("class (\w+\\n)", content)
    if match is None:
        print("Could not detect class in file '"+file+"'")
        return -1
    
    return match.group(1).strip()

def compile(file, directory):
    if(file['extension'] not in _LANGUAGE_COMPILE_COMMANDS):
        print("Files of this type should not be compiled")
        return -1
    print("Compiling " + file['name'])
    cmd = [formatCommand(p, file) for p in _LANGUAGE_COMPILE_COMMANDS[file['extension']]]
    subprocess.run(cmd, cwd=directory)

def shouldCompile(file):
    return file['extension'] in _LANGUAGE_COMPILE_COMMANDS

def getBytesFromFile(file):
    inFile = open(file, "rb")
    result = inFile.read()
    inFile.close()
    return result

