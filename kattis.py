import sys, os, requests, zipfile, io, shutil, subprocess

def getBytesFromFile(file):
    inFile = open(file, "rb")
    result = inFile.read()
    inFile.close()
    return result


def get(args):
    if(os.path.exists(args[0])):
        print("You have already gotten this problem!")
        return
    r = requests.get("https://open.kattis.com/problems/" + args[0] + "/file/statement/samples.zip", stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    os.makedirs(args[0])
    z.extractall(args[0] + "/test")
    shutil.copy2("boilerplate.py", args[0] + "/" + args[0] + ".py")
    print("Successfully initialized exercise", args[0] + "!")
    print("You can test your script with 'kattis test " + args[0] + "'")

def submit(args):
    subprocess.run(["py", "submit.py", "-p", args[0], ".\\" + args[0] + "\\" + args[0] + ".py"])

def test(args):
    testPath = args[0] + "/test"
    files = [f for f in os.listdir(testPath) if os.path.isfile(os.path.join(testPath, f))]
    inFiles = [testPath + "/" + f for f in files if f.endswith(".in")]
    ansFiles = [testPath + "/" + f for f in files if f.endswith(".ans")]
    for inF, ansF in zip(inFiles, ansFiles):
        input = getBytesFromFile(inF)
        answer = getBytesFromFile(ansF).decode("utf-8")
        result = subprocess.run(["py",args[0]+"/"+args[0]+".py"], stdout=subprocess.PIPE, input=input).stdout.decode("utf-8").replace("\r\n", "\n")
        if (answer == result):
            print("\U0001F49A", inF, "succeeded")
        else:
            print("\U0000274C", inF, "failed")
            print("expected:")
            print(answer)
            print("actual:")
            print(result)
        print()

def help(args):
    print("Available Commands:")
    print("get: Downloads the sample input-output files for the problem and creates a directory for the problem.")
    print("submit: Submits your work to kattis for judgement.")
    print("test: Runs your program locally using the downloaded .in files and compares them with the .ans files.")

def main():
    command = sys.argv[1] if sys.argv[1:] else ''
    args = sys.argv[2:]
    if command == "get":
        get(args)
    elif command == "submit":
        submit(args)
    elif command == "test":
        test(args)
    elif command == "help":
        help(args)
    else: 
        print("Whoops, did not recognize command", command)
        help(args)
        return
    

main()