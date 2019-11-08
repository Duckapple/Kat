import os, requests, zipfile, io, shutil

from commands.open import openCommand
from enum import Enum, auto

from helpers.cli import yes
from helpers.exceptions import RedundantCommandException, InvalidProblemException
from helpers.webutils import checkProblemExistence


class GetResponse(Enum):
    Success = auto()
    Failure = auto()
    Redundant = auto()


def getCommand(problemName, options):
    if os.path.exists(problemName) or os.path.exists(".archive/" + problemName) or os.path.exists(".solved/" + problemName):
        raise RedundantCommandException("⚠️ You have already gotten problem " + problemName + "!")

    problemUrl = "https://open.kattis.com/problems/" + problemName

    checkProblemExistence(problemName)

    print("🧰  Initializing problem " + problemName)

    os.makedirs(problemName)
    downloadSampleFiles(problemName, problemUrl)
    createBoilerplate(problemName)

    print("👍 Successfully initialized exercise", problemName + "!")
    print("   You can test your script with 'kattis test " + problemName + "'")
    if "open" in options:
        openCommand(problemName)
    return GetResponse.Success


def promptToGet(arg, options):
    print("This problem is not present...")
    print("Do you want to get it?")
    if yes():
        print("Getting problem...")
        getCommand(arg, options)


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
        os.path.dirname(os.path.realpath(__file__)) + "/../boilerplate/boilerplate.py",
        problemName + "/" + problemName + ".py",
    )

getFlags = [
    ("open", False),
]