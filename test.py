import os, subprocess
import re
from get import promptToGet

_LANGUAGE_COMMANDS = {
    '.py': ['python3', '@f'],
    '.php': ['php', '@f'],
    # TODO: Figure out how to pass class name to java and possibly compile the class beforehand
    '.java': ['java', '@c'],
    # TODO: Support rest of the languages that kattis supports
}

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

_REQUIRES_CLASS = [
    '.java'
]

def test(args, options):
    problemName = args[0]

    if not os.path.exists(problemName):
        promptToGet(args, options)
        return
    
    testPath = problemName + "/test"
    files = [f for f in os.listdir(testPath) if os.path.isfile(os.path.join(testPath, f))]
    inFiles = [testPath + "/" + f for f in files if f.endswith(".in")]
    ansFiles = [testPath + "/" + f for f in files if f.endswith(".ans")]
    passed = True
    
    programFile = args[1] if args[1:] else getSourceFile(problemName)
    if(programFile == -1):
        return
    
    command = getCommand(problemName, programFile)

    if(command == -1):
        return

    for inF, ansF in zip(inFiles, ansFiles):
        answer = getBytesFromFile(ansF).decode("utf-8")
        result = runSingleTest(command, inF, problemName)
        if (answer == result):
            print("\U0001F49A", inF, "succeeded")
        else:
            passed = False
            print("\U0000274C", inF, "failed")
            print("expected:")
            print(answer)
            print("actual:")
            print(result)
    
    if passed and "-a" in options:
        archive(args, options)

def runSingleTest(command, inFile, problemName):
    inp = getBytesFromFile(inFile)
    directory = os.path.join(os.getcwd(), problemName)
    return subprocess.run(command, stdout=subprocess.PIPE, input=inp, cwd=directory).stdout.decode("utf-8").replace("\r\n", "\n")

def getSourceFile(problemName):
    files = [f for f in os.listdir(problemName) if isValidSourceFile(problemName, f)]
    
    if(len(files) == 0):
        print("No source file fould for problem '" + problemName + "'.\nCreate a file inside the folder matching the problem (for example '"+problemName+"/answer.py')")
        return -1
    
    if(len(files) > 1):
        print("Multiple source files found. Choose one:")
        i = 0
        for f in files:
            extension = os.path.splitext(f)[1]
            language = _LANGUAGE_GUESS[extension]
            print(str(i+1)+") " + f + " ("+language+")")
            i+=1
        chosen = files[int(input()) - 1]
        print("Running tests on " + chosen)
        return chosen
    
    return files[0]

def isValidSourceFile(dir, file):
    p = os.path.join(dir, file)
    extension = os.path.splitext(file)[1]
    return os.path.isfile(p) and extension in _LANGUAGE_COMMANDS

def getCommand(dir, file):
    [basename, extension] = os.path.splitext(file)
    if(extension not in _LANGUAGE_COMMANDS):
        print("Unsupported programming language")
        return -1
    cmd = _LANGUAGE_COMMANDS[extension]
    className = "" if extension not in _REQUIRES_CLASS else detectClassName(dir, file)
    if(className == -1):
        return -1
    return [p.replace("@f", file).replace("@c", className) for p in cmd]
    
def detectClassName(dir, file):
    content = getBytesFromFile(os.path.join(dir, file)).decode("utf-8")
    extension = os.path.splitext(file)[1]
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

