import io, os, requests, traceback, webbrowser, zipfile
from urllib import parse
from helpers.exceptions import InvalidProblemException
from helpers.fileutils import createBoilerplate
from helpers.cli import yes
from helpers.config import getConfigUrl

HEADERS = {"User-Agent": "Kat"}

def checkProblemExistence(problemName):
    problemUrl = getProblemUrl(problemName)
    existenceTest = requests.get(problemUrl)
    if existenceTest.status_code != 200:
        raise InvalidProblemException("⚠️ Problem '" + problemName + "' does not exist!")


def fetchProblem(problemName, overrideLanguage = None):
    problemUrl = getProblemUrl(problemName)
    checkProblemExistence(problemName)
    print("🧰  Initializing problem " + problemName)
    os.makedirs(problemName)
    downloadSampleFiles(problemName, problemUrl)
    createBoilerplate(problemName, overrideLanguage)

def getProblemUrl(problemName):
    return getConfigUrl("problemsurl", "problems") + "/" + problemName

def promptToFetch(problemName):
    print("This problem is not present...")
    print("Do you want to get it?")
    if yes():
        print("Getting problem...")
        fetchProblem(problemName)


def downloadSampleFiles(problemName, problemUrl):
    r = requests.get(problemUrl + "/file/statement/samples.zip", stream=True)
    if r.status_code != 200:
        print("🤷 No sample files for this problem")
        return
    print("⬇️  Attempting to download sample files from kattis...")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(problemName + "/test")

def submitError(e: Exception):
    body = parse.quote_plus('\n\n```\n' + ''.join(traceback.format_exception(None, e, e.__traceback__)) + '\n```')
    webbrowser.open(f"https://github.com/Duckapple/Kat/issues/new?body={body}&title=Exception%3A%20%22{str(e)}%22")


def checkCorrectDomain(problemName, commandName):
    if "." in problemName:
        hostPrefix = problemName.split(".")[0]
        hostname = hostPrefix + ".kattis.com"
        cfg = getConfig()
        actualHostname = cfg["kattis"]["hostname"]
        if hostname != actualHostname:
            print(f'Warning: The problem you are trying to {commandName} looks like it is part of the subdomain "{hostname}", '
                  f'while your instance of Kat tool currently uses "{actualHostname}". Would you like to switch '
                  f'beforehand?')
            if yes():
                cfg["kattis"]["hostname"] = hostname
                saveConfig()