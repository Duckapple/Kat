import os, subprocess

from get import promptToGet

def getBytesFromFile(file):
    inFile = open(file, "rb")
    result = inFile.read()
    inFile.close()
    return result

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
        result = subprocess.run(["python3", args[0]+"/"+args[0]+".py"], stdout=subprocess.PIPE, input=input).stdout.decode("utf-8").replace("\r\n", "\n")
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