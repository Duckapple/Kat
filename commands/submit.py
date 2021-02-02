import os, requests, sys, re, time
from enum import Enum, auto

from bs4 import BeautifulSoup
from helpers.cli import yes
from commands.web import openSubmission
from helpers.webutils import promptToFetch
from helpers.programSelector import (
    formatProgramFile,
    selectProgramFile,
    guessLanguage,
    requiresClass,
    detectClassName,
)
from helpers.auth import login
from helpers.config import getConfig, getUrl
from commands.archive import archiveCommand
from helpers.sound import losesound, winsound
from helpers.fileutils import undoBOM


class Response(Enum):
    Success = auto()
    Failure = auto()
    Error = auto()
    Aborted = auto()


_HEADERS = {"User-Agent": "Kat"}

_ERROR_MESSAGES = {
    "Wrong Answer": "💔 Wrong Answer on @test of @total",
    "Run Time Error": "💥 Run Time Error on @test of @total",
    "Time Limit Exceeded": "⌛ Time Limit Exceeded on @test of @total",
    "Memory Limit Exceeded": "🙀 Memory Limit Exceeded on  @test of @total",
    "Output Limit Exceeded": "🙀 Output Limit Exceeded on  @test of @total",
    "Judge Error": "❗ The near-impossible has happened! Kattis reported a 'Judge Error' while processing your submission. You should probably contact them.",
    "Compile Error": "⛔ Your submission had a 'Compile Error' while being tested.",
}


def submitCommand(args, options):
    problemName = args[0]
    directory = os.path.join(os.getcwd(), problemName)

    if not os.path.exists(problemName):
        promptToFetch(args, options)
        return Response.Error

    # if programFile is not given, we will attempt to guess it
    programFile = (
        formatProgramFile(args[1]) if args[1:] else selectProgramFile(problemName)
    )

    if programFile == -1:
        raise Exception("Could not guess programFile")

    if "force" not in options:
        response = confirm(problemName, programFile)
        if not response: return Response.Aborted

    config = getConfig()

    session = requests.Session()

    print("📨 Submitting " + problemName + "...")

    id = postSubmission(config, session, problemName, programFile)

    print(
        "📬 Submission Successful (url " + getUrl(config, "submissionsurl", "submissions") + "/" + id + ")"
    )

    if id == -1:
        return False

    response = Response.Failure
    try:
        response = printUntilDone(id, problemName, config, session, options)
    except:
        pass
    if "sound" in options:
        if response == Response.Success:
            winsound()
        elif response == Response.Failure:
            losesound()
    if response == Response.Success:
        if "archive" in options:
            archiveCommand(problemName, options, ".solved/")
    return response



def confirm(problemName, programFile):
    print("Are you sure you want to submit?")
    print("Problem: " + problemName)
    print("File: " + programFile["relativePath"])
    print("Language: " + guessLanguage(programFile))

    return yes()


def postSubmission(config, session, problemName, programFile):
    login(config, session)

    url = getUrl(config, "submissionurl", "submit")
    language = guessLanguage(programFile)

    if language == -1:
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

    response = session.post(url, data=data, files=sub_files, headers=_HEADERS)

    body = response.content.decode("utf-8").replace("<br />", "\n")
    match = re.search(r"Submission ID: ([0-9]+)", body)

    if match is None:
        print(
            "Submission was received, but could not read ID from response. Visit the submission manually in the browser."
        )
        print("Response was: " + body)
        return -1

    return match.group(1).strip()


def printUntilDone(id, problemName, config, session, options):
    lastCount = 0
    spinnerParts = ["-", "\\", "|", "/"]

    print("⚖️  Submission Status:")

    while True:
        login(config, session)
        response, data = fetchNewSubmissionStatus(id, session, config, options)
        if response != Response.Success:
            return response
        if "status" in data:
            status = data["status"]
            lastCount += 1
            print(status, spinnerParts[lastCount % 4], end="\r")
            sys.stdout.flush()
            if status == "Accepted":
                print("\r💚                ") # clear line
                break
        else:
            for _ in range(0, abs(lastCount - data["testCount"])):
                sys.stdout.write("💚")
            sys.stdout.flush()

            if data["testTotal"] != 0 and data["testCount"] == data["testTotal"]:
                break

            lastCount = data["testCount"]

        time.sleep(1)

    print()
    print(
        "🎉 Congratulations! You completed all ",
        (str(data["testTotal"]) if "testTotal" in data else ""),
        " tests for ",
        problemName
    )
    return Response.Success


def fetchNewSubmissionStatus(id, session, cfg, options):
    response = session.get(
        getUrl(cfg, "submissionsurl", "submissions") + "/" + id, headers=_HEADERS
    )

    body = response.content.decode("utf-8")
    soup = BeautifulSoup(body, "html.parser")
    data = soup.select("#judge_table tbody tr")
    info = data[0]
    testcases = data[1] if len(data) > 1 else None

    status = info.select_one("td.status").text

    if status == "Compile Error":
        print(_ERROR_MESSAGES["Compile Error"])
        raise Exception(_ERROR_MESSAGES["Compile Error"])

    if not testcases:
        return Response.Success, {"status": status}

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

    return Response.Success, {"testCount": successCount, "testTotal": int(testTotal)}


def formatLanguage(language):
    if language == "Python":
        return formatPythonLanguage(language)

    return language


def formatPythonLanguage(language):
    python_version = str(sys.version_info[0])

    if python_version not in ["2", "3"]:
        print("python-version in .kattisrc must be 2 or 3")
        raise Exception("python-version in .kattisrc must be 2 or 3")

    return "Python " + python_version


submitFlags = [
    ("archive", False),
    ("force", False),
    ("sound", False),
]
