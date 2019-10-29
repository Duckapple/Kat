import os, requests, zipfile, io, shutil

from open import openCommand


def get(args, options):
    for arg in args:
        getProblem(arg, options)


def getProblem(problemName, options):
    if os.path.exists(problemName) or os.path.exists(".archive/" + problemName):
        print("⚠️ You have already gotten problem " + problemName + "!")
        return

    problemUrl = "https://open.kattis.com/problems/" + problemName

    existenceTest = requests.get(problemUrl)
    if existenceTest.status_code != 200:
        print("⚠️ Problem does not exist!")
        return

    print("🧰  Initializing problem " + problemName)

    os.makedirs(problemName)
    downloadSampleFiles(problemName, problemUrl)
    createBoilerplate(problemName)

    print("👍 Successfully initialized exercise", problemName + "!")
    print("   You can test your script with 'kattis test " + problemName + "'")
    if "-o" in options:
        openCommand(problemName)


def promptToGet(args, options):
    print("This problem is not present...")
    print("Do you want to get it?")
    if yes():
        print("Getting problem...")
        get(args, options)


def downloadSampleFiles(problemName, problemUrl):
    r = requests.get(problemUrl + "/file/statement/samples.zip", stream=True)
    if r.status_code != 200:
        print("🤷 No sample files for this problem")
        return
    print("⬇️  Attempting to download sample files from kattis...")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(problemName + "/test")


def createBoilerplate(problemName):
    shutil.copy2(
        os.path.dirname(os.path.realpath(__file__)) + "/boilerplate.py",
        problemName + "/" + problemName + ".py",
    )
