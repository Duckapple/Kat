import os, requests, zipfile, io, shutil


def get(args, forced):
    for arg in args:
        getProblem(arg)


def getProblem(problemName):
    if os.path.exists(problemName) or os.path.exists(".archive/" + problemName):
        print("⚠️ You have already gotten problem " + problemName + "!")
        return
    problem = "https://open.kattis.com/problems/" + problemName
    existenceTest = requests.get(problem)
    if existenceTest.status_code != 200:
        print("⚠️ Problem does not exist!")
        return
    print("⬇️  Attempting to download exercise from kattis...")
    r = requests.get(problem + "/file/statement/samples.zip", stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    os.makedirs(problemName)
    z.extractall(problemName + "/test")
    shutil.copy2(
        os.path.dirname(os.path.realpath(__file__)) + "/boilerplate.py",
        problemName + "/" + problemName + ".py",
    )
    print("👍 Successfully initialized exercise", problemName + "!")
    print("   You can test your script with 'kattis test " + problemName + "'")


def promptToGet(args, options):
    print("This problem is not present...")
    print("Do you want to get it?")
    if yes():
        print("Getting problem...")
        get(args, options)


def yes():
    answer = input("(y/N): ").lower()
    return answer == "y" or answer == "yes"
