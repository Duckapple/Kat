import os, requests, sys, re, json, time
from get import promptToGet
from programSelector import (
    formatProgramFile,
    selectProgramFile,
    guessLanguage,
    requiresClass,
    detectClassName,
)
from config import getConfig, getUrl, formatUrl
from bs4 import BeautifulSoup

_HEADERS = {"User-Agent": "Kat"}


def submit(args, options):
    problemName = args[0]
    directory = os.path.join(os.getcwd(), problemName)

    if not os.path.exists(problemName):
        promptToGet(args, options)
        return

    # if programFile is not given, we will attempt to guess it
    programFile = (
        formatProgramFile(args[1]) if args[1:] else selectProgramFile(problemName)
    )

    if programFile == -1:
        return

    config = getConfig()

    session = requests.Session()

    print("📨 Submitting " + problemName + "...")

    id = postSubmission(config, session, problemName, programFile)

    print(
        "📬 Submission Successfull (url https://open.kattis.com/submissions/" + id + ")"
    )

    if id == -1:
        return

    printUntilDone(id, problemName, config, session)


def login(config, session):
    username = config.get("user", "username")
    token = config.get("user", "token")
    login_url = getUrl(config, "loginurl", "login")

    session.post(
        login_url,
        data={"user": username, "token": token, "script": "true"},
        headers=_HEADERS,
    )


def postSubmission(config, session, problemName, programFile):
    login(config, session)

    url = getUrl(config, "submissionurl", "submit")
    language = guessLanguage(programFile)

    if language == -1:
        print("Could not guess language for " + programFile)
        return -1

    data = {
        "submit": "true",
        "submit_ctr": 2,
        "language": formatLanguage(language),
        "problem": problemName,
        "script": "true",
    }

    if requiresClass(programFile):
        data["mainclass"] = detectClassName(programFile)

    sub_files = []
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


def printUntilDone(id, problemName, config, session):
    lastTotal = 0
    lastCount = 0

    print("⚖️  Submission Status:")

    while True:
        login(config, session)
        testCount, testTotal = fetchNewSubmissionStatus(id, session, config)

        for i in range(0, abs(lastCount - testCount)):
            sys.stdout.write("💚")
        sys.stdout.flush()

        if testTotal != 0 and testCount == testTotal:
            break

        lastTotal = testTotal
        lastCount = testCount
        time.sleep(1)

    print()
    print(
        "🎉 Congratulations! You completed all "
        + str(testTotal)
        + " tests for "
        + problemName
    )


def fetchNewSubmissionStatus(id, session, cfg):
    response = session.get(
        "https://open.kattis.com/submissions/" + id, headers=_HEADERS
    )

    body = response.content.decode("utf-8")
    soup = BeautifulSoup(body, "html.parser")
    [info, testcases] = soup.select("#judge_table tbody tr")

    status = info.select_one("td.status")

    if status.text == "Compile Error":
        print("⛔ Your submission had a 'Compile Error' while being tested.")
        sys.exit(1)

    successCount = 0
    testTotal = 0

    for testcase in testcases.select(".testcases > span"):
        testResult = testcase.get("title")
        match = re.search(r"Test case (\d+)\/(\d+): (.+)", testResult)
        if match is None:
            print(
                "⚠️ Error while parsing test cases. Please report this on our github so we can fix it in future versions."
            )
            sys.exit(1)
        testNumber = match.group(1)
        testTotal = match.group(2)
        testStatus = match.group(3)

        if testStatus == "Accepted":
            successCount += 1
        elif testStatus == "not checked":
            break
        elif testStatus == "Wrong Answer":
            print("\U0000274C\n💔 Wrong Answer on " + testNumber + " of " + testTotal)
            sys.exit(1)
        elif testStatus == "Run Time Error":
            print("\U0000274C\n💥 Run Time Error on " + testNumber + " of " + testTotal)
            sys.exit(1)
        elif testStatus == "Time Limit Exceeded":
            print(
                "\U0000274C\n⌛ Time Limit Exceeded on "
                + testNumber
                + " of "
                + testTotal
            )
            sys.exit(1)
        elif testStatus == "Memory Limit Exceeded":
            print(
                "\U0000274C\n🙀 Memory Limit Exceeded on "
                + testNumber
                + " of "
                + testTotal
            )
            sys.exit(1)
        elif testStatus == "Output Limit Exceeded":
            print(
                "\U0000274C\n🙀 Output Limit Exceeded on "
                + testNumber
                + " of "
                + testTotal
            )
            sys.exit(1)
        elif testStatus == "Judge Error":
            print(
                "\U0000274C\n❗ The near-impossible has happened! Kattis reported a 'Judge Error' while processing your submission. You should probably contact them."
            )
            sys.exit(1)
        else:
            print(
                "⚠️\n😕 Unknown error  '"
                + testStatus
                + "' for test case. Please report this on our github so we can fix it in future versions"
            )
            sys.exit(1)

    return successCount, int(testTotal)


def formatLanguage(language):
    if language == "Python":
        return formatPythonLanguage(language)

    return language


def formatPythonLanguage(language):
    python_version = str(sys.version_info[0])

    if python_version not in ["2", "3"]:
        print("python-version in .kattisrc must be 2 or 3")
        sys.exit(1)

    return "Python " + python_version
