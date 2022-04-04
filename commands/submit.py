from argparse import ArgumentParser
import os, requests, sys, re, time
from enum import Enum, auto

from bs4 import BeautifulSoup
from helpers.cli import yes
from helpers.types import problem
from helpers.webutils import HEADERS, promptToFetch, checkCorrectDomain
from helpers.programSelector import (
    formatProgramFile,
    selectProgramFile,
    guessLanguage,
    requiresClass,
    detectClassName,
)
from helpers.auth import login
from helpers.config import getConfig, getConfigUrl
from commands.archive import archive
from helpers.sound import losesound, winsound
from helpers.fileutils import undoBOM


class Response(Enum):
    Success = auto()
    Failure = auto()
    Error = auto()
    Aborted = auto()

_ERROR_MESSAGES = {
    "Wrong Answer": "💔 Wrong Answer on @test of @total",
    "Run Time Error": "💥 Run Time Error on @test of @total",
    "Time Limit Exceeded": "⌛ Time Limit Exceeded on @test of @total",
    "Memory Limit Exceeded": "🙀 Memory Limit Exceeded on @test of @total",
    "Output Limit Exceeded": "🙀 Output Limit Exceeded on @test of @total",
    "Judge Error": "❗ The near-impossible has happened! Kattis reported a 'Judge Error' while processing your submission. You should probably contact them.",
    "Compile Error": "⛔ Your submission had a 'Compile Error' while being tested.",
}


def submitCommand(data):
    problemName: str = data["problem"]
    checkCorrectDomain(problemName, "submit")

    if not os.path.exists(problemName):
        promptToFetch(problemName)
        return Response.Error

    # if programFile is not given, we will attempt to guess it
    programFile = (
        formatProgramFile(data.get("file")) if data.get("file") else selectProgramFile(problemName)
    )

    if programFile == None:
        raise Exception("Could not guess programFile")

    if "force" not in data or not data.get('force'):
        response = confirm(problemName, programFile)
        if not response: return Response.Aborted
    try:
        session = requests.Session()

        print("📨 Submitting " + problemName + "...")

        id = postSubmission(session, problemName, programFile)

        print(
            f"📬 Submission Successful (url {getConfigUrl('submissionsurl', 'submissions')}/{id})"
        )

        if id == None:
            return False

        response = Response.Failure
        try:
            response = printUntilDone(id, problemName, session)
        except:
            pass
        if data.get('sound'):
            if response == Response.Success:
                winsound()
            elif response == Response.Failure:
                losesound()
        if response == Response.Success:
            if data.get('archive'):
                archive(problemName, ".solved/")
        return response

    except requests.exceptions.ConnectionError:
        print("Connection error: Please check your connection")
        return Response.Error


def confirm(problemName, programFile):
    print("Are you sure you want to submit?")
    print("Problem: " + problemName)
    print("File: " + programFile["relativePath"])
    print("Language: " + guessLanguage(programFile))

    return yes(defaultToYes= True)


def postSubmission(session, problemName, programFile):
    login(session)

    url = getConfigUrl("submissionurl", "submit")
    language = guessLanguage(programFile)

    if language == None:
        print("Could not guess language for " + programFile)
        raise Exception("Could not guess language for " + programFile)

    language = formatLanguage(language)
    data = {
        "submit": "true",
        "submit_ctr": 2,
        "language": language,
        "problem": problemName,
        "script": "true",
    }

    if requiresClass(programFile):
        data["mainclass"] = detectClassName(programFile)

    sub_files = []
    undoBOM(programFile["relativePath"])
    with open(programFile["relativePath"]) as sub_file:
        sub_files.append(
            (
                "sub_file[]",
                (programFile["name"], sub_file.read(), "application/octet-stream"),
            )
        )

    response = session.post(url, data=data, files=sub_files, headers=HEADERS)

    body = response.content.decode("utf-8").replace("<br />", "\n")
    match = re.search(r"Submission ID: ([0-9]+)", body)

    if match is None:
        print(
            "Submission was received, but could not read ID from response.",
            "Visit the submission manually in the browser.",
        )
        print("Response was: " + body)
        return None

    return match.group(1).strip()

def printFinalStatus(status, icon, runtime):
    print(f"\r{icon} {status} ({runtime})")

def printUntilDone(id, problemName, session):
    lastCount = 0
    spinnerParts = ["-", "\\", "|", "/"]
    runtime = None

    print("⚖️  Submission Status:")

    while True:
        login(session)
        response, data = fetchNewSubmissionStatus(id, session)
        if response != Response.Success:
            return response
        if data.get('status'):
            status = data.get('status')
            lastCount += 1
            print(status, spinnerParts[lastCount % 4], end="\r")
            sys.stdout.flush()

            if status == "Accepted" or status == "Accepted (100)":
                runtime = data.get("runtime") or getRuntime(id, problemName, session)
                printFinalStatus("💚", status, runtime)
                break
            if status.startswith("Accepted"):
                runtime = data.get("runtime") or getRuntime(id, problemName, session)
                printFinalStatus("🟨", status, runtime)
                break
            if status in _ERROR_MESSAGES.keys():
                runtime = data.get("runtime") or getRuntime(id, problemName, session)
                print(f"{_ERROR_MESSAGES[status].replace(' on @test of @total', '')} ({runtime})")
                return Response.Error
        else:
            for _ in range(0, abs(lastCount - data["testCount"])):
                sys.stdout.write("💚")
            sys.stdout.flush()

            if data["testTotal"] != 0 and data["testCount"] == data["testTotal"]:
                runtime = data.get("runtime")
                break

            lastCount = data["testCount"]

        time.sleep(0.5)

    if not runtime:
        runtime = getRuntime(id, problemName, session)

    print()
    print(
        "🎉 Congratulations! You completed all",
        f"{str(data['testTotal']) + ' ' if 'testTotal' in data else ''}tests for",
        f"{problemName}{f' in {runtime}' if runtime else ''}!"
    )
    return Response.Success

def fetchNewSubmissionStatus(id, session):
    response = session.get(
        getConfigUrl("submissionsurl", "submissions") + "/" + id, headers=HEADERS
    )

    body = response.content.decode("utf-8")
    soup = BeautifulSoup(body, "html.parser")
    data = soup.select("#judge_table tbody tr")
    info = data[0]
    testcases = data[1] if len(data) > 1 else None

    status = info.select_one("td.status").text
    runtime = info.select("td.runtime")
    runtime = runtime[0].text if len(runtime) >= 1 else None

    if status == "Compile Error":
        print(_ERROR_MESSAGES["Compile Error"])
        raise Exception(_ERROR_MESSAGES["Compile Error"])

    if not testcases:
        return Response.Success, {"status": status, "runtime": runtime}

    successCount = 0
    testTotal = 0

    for testcase in testcases.select(".testcases > span"):
        testResult = testcase.get("title")
        match = re.search(r"Test case (\d+)\/(\d+): (.+)", testResult)
        if match is None:
            print(
                "⚠️ Error while parsing test cases. Please report this on our github so we can fix it in future versions."
            )
            raise Exception("⚠️ Error while parsing test cases. Please report this on our github so we can fix it in future versions.")
        testNumber = match.group(1)
        testTotal = match.group(2)
        testStatus = match.group(3).strip()

        if testStatus == "Accepted":
            successCount += 1
        elif testStatus == "not checked":
            break
        elif testStatus in _ERROR_MESSAGES:
            msg = (
                _ERROR_MESSAGES[testStatus]
                .replace("@test", testNumber)
                .replace("@total", testTotal)
            )
            print("\U0000274C\n" + msg)
            return Response.Failure
        else:
            print(
                "⚠️\n😕 Unknown error  '"
                + testStatus
                + "' for test case. Please report this on our github so we can fix it in future versions"
            )
            raise Exception("Unknown Error")

    return Response.Success, {"testCount": successCount, "testTotal": int(testTotal), "runtime": runtime}

def getRuntime(id, problemName, session):
    user = getConfig().get("user", {})
    username = user.get("username")
    url = f"{getConfigUrl('usersurl', 'users')}/{username}/submissions/{problemName}"
    response = session.get(
        url, headers=HEADERS
    )
    body = response.content.decode("utf-8")
    soup = BeautifulSoup(body, "html.parser")
    data = soup.select(f'table.table-kattis tbody tr[data-submission-id="{id}"] td.runtime')
    if len(data) > 0:
        return data[0].text

def formatLanguage(language):
    if language == "python":
        return formatPythonLanguage()

    return language


def formatPythonLanguage():
    python_version = str(sys.version_info[0])

    if python_version not in ["2", "3"]:
        print("python-version in .kattisrc must be 2 or 3")
        raise Exception("python-version in .kattisrc must be 2 or 3")

    return "Python " + python_version

def submitParser(parsers: ArgumentParser):
    helptext = 'Submit a problem for evaluation.'
    parser = parsers.add_parser('submit', description=helptext, help=helptext)
    parser.add_argument('problem', help='Name of problem to submit', type=problem)
    parser.add_argument('file', nargs='?', help='Name of the specific file to submit')
    submitFlags(parser)

def submitFlags(parser):
    parser.add_argument('-a', '--archive', action='store_true', help='Archive the problem on a successful submittion.')
    parser.add_argument('-f', '--force', action='store_true', help='Force a submit of the first detected program file.')
    parser.add_argument('-s', '--sound', action='store_true', help='Play a sound on successful submittion.')
