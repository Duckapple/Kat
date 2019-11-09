import io
import os
import zipfile

import requests

from helpers.fileutils import createBoilerplate
from helpers.cli import yes


def checkProblemExistence(problemName):
    problemUrl = "https://open.kattis.com/problems/" + problemName
    existenceTest = requests.get(problemUrl)
    if existenceTest.status_code != 200:
        raise InvalidProblemException("⚠️ Problem '" + problemName + "' does not exist!")


def fetchProblem(problemName):
    problemUrl = "https://open.kattis.com/problems/" + problemName
    checkProblemExistence(problemName)
    print("🧰  Initializing problem " + problemName)
    os.makedirs(problemName)
    downloadSampleFiles(problemName, problemUrl)
    createBoilerplate(problemName)


def promptToFetch(arg, options):
    print("This problem is not present...")
    print("Do you want to get it?")
    if yes():
        print("Getting problem...")
        fetchProblem(arg)


def downloadSampleFiles(problemName, problemUrl):
    r = requests.get(problemUrl + "/file/statement/samples.zip", stream=True)
    if r.status_code != 200:
        print("🤷 No sample files for this problem")
        return
    print("⬇️  Attempting to download sample files from kattis...")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(problemName + "/test")