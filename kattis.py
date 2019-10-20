import sys, os, requests, zipfile, io, shutil, subprocess

def printUsage():
    print("Usage: kattis [<OPTIONS>] <COMMAND> <ARGS>")

def printFullUsage():
    printUsage()
    print()
    print("COMMAND:")
    print("  get      Gets the argument problem test cases and prepares boilerplate")
    print("  test     Tests the argument problem against all test files")
    print("  submit   Submits the argument problem to the Kattis servers")
    print("  archive  Archives the problem in the \".archive\"-folder")
    print("OPTIONS:")
    print("  -f       Force the action directly (applies to <submit>)")
    print("  -h       Prints the help message for the typed command")
    print("  -a       Archives the problem after executing the command (applies to <submit> and <test>)")

def printHelp(command):
    string = helpCommand.get(command, "")
    if string == "":
        printFullUsage()
    else:
        print(string)

def yes():
    answer = input("(y/N): ").lower()
    return answer == "y" or answer == "yes"

def divideArgs(args):
    arg = []
    options = []
    for word in args:
        if ("-" in word):
            options.append(word)
        else:
            arg.append(word)
    return arg, options



def getBytesFromFile(file):
    inFile = open(file, "rb")
    result = inFile.read()
    inFile.close()
    return result


def promptToGet(args, options):
    print("This problem is not present...")
    print("Do you want to get it?")
    if yes():
        print("Getting problem...")
        get(args, options)


def get(args, forced):
    if (os.path.exists(args[0]) or os.path.exists(".archive/" + args[0])):
        print("You have already gotten this problem!")
        return
    problem = "https://open.kattis.com/problems/" + args[0]
    existenceTest = requests.get(problem)
    if existenceTest.status_code != 200:
        print("Problem does not exist!")
        return
    r = requests.get(problem + "/file/statement/samples.zip", stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    os.makedirs(args[0])
    z.extractall(args[0] + "/test")
    shutil.copy2("boilerplate.py", args[0] + "/" + args[0] + ".py")
    print("Successfully initialized exercise", args[0] + "!")
    print("You can test your script with 'kattis test " + args[0] + "'")

def submit(args, options):
    command = ["py", "submit.py", "-p", args[0], ".\\" + args[0] + "\\" + args[0] + ".py"]
    if "-f" in options:
        command.append("-f")
    subprocess.run(args=command)
    if "-a" in options:
        archive(args, options)

def test(args, options):
    if not os.path.exists(args[0]):
        promptToGet(args, options)
        return
    testPath = args[0] + "/test"
    files = [f for f in os.listdir(testPath) if os.path.isfile(os.path.join(testPath, f))]
    inFiles = [testPath + "/" + f for f in files if f.endswith(".in")]
    ansFiles = [testPath + "/" + f for f in files if f.endswith(".ans")]
    passed = True
    for inF, ansF in zip(inFiles, ansFiles):
        input = getBytesFromFile(inF)
        answer = getBytesFromFile(ansF).decode("utf-8")
        result = subprocess.run(["py",args[0]+"/"+args[0]+".py"], stdout=subprocess.PIPE, input=input).stdout.decode("utf-8").replace("\r\n", "\n")
        if (answer == result):
            print("\U0001F49A", inF, "succeeded")
        else:
            passed = False
            print("\U0000274C", inF, "failed")
            print("expected:")
            print(answer)
            print("actual:")
            print(result)
        print()
    
    if passed and "-a" in options:
        archive(args, options)

def archive(args, options):
    if os.path.exists(".archive/" + args[0]):
        print("You have already archived this problem.")
        return
    if not os.path.exists(args[0]):
        promptToGet(args, options)
        return
    shutil.move(args[0], ".archive/" + args[0])
    print("Moved problem", args[0], "to archive")

execCommand = {
    "archive": archive,
    "get": get,
    "submit": submit,
    "test": test
}

helpCommand = {
    "archive": """
Usage: kattis [<options>] archive <problem>

    Archives the problem in the \".archive\"-folder""",
    
    "get": """
Usage: kattis [<options>] get <problem>

    Gets the argument problem test cases and prepares boilerplate""",

    "submit": """
Usage: kattis [<options>] submit <problem>

    Submits the argument problem to the Kattis servers

Options:
    -a    Archives the problem after executing the command
    -f    Force the action directly""",

    "test": """
Usage: kattis [<options>] test <problem>

    Tests the argument problem against all test files

Options:
    -a    Archives the problem after executing the command"""
}

def helpIfNotCommandInner(args, options):
    print("Whoops, did not recognize that command.") 
    printUsage()

def helpIfNotCommand(command):
    return helpIfNotCommandInner

def main():
    args, options = divideArgs(sys.argv)
    helpy = "-h" in options
    command = args[1]
    args = args[2:]

    if (helpy):
        printHelp(command)
    else: 
        execCommand.get(command, helpIfNotCommand(command))(args, options)
    

main()