import os, requests
from get import promptToGet
from programSelector import formatProgramFile, selectProgramFile, guessLanguage
from config import getConfig

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

    [cookies] = login(config)

    submit_url = getUrl(config, "submissionurl", "submit")

    id = postSubmission(submit_url, cookies, problemName, programFile)
    print(id)
    if id == -1:
        return


def login(config):
    username = config.get("user", "username")
    token = config.get("user", "token")
    login_url = getUrl(config, "loginurl", "login")

    data = {"user": username, "token": token, "script": "true"}

    return requests.post(login_url, data=data, headers=_HEADERS)


def postSubmission(url, cookies, problemName, programFile):
    language = guessLanguage(programFile)
    if language == -1:
        print("Could not guess language for " + programFile)
        return -1

    data = {
        "submit": "true",
        "submit_ctr": 2,
        "language": language,
        "mainclass": mainclass,
        "problem": problemName,
        "script": "true",
    }

    sub_files = []
    for f in files:
        with open(f) as sub_file:
            sub_files.append(
                (
                    "sub_file[]",
                    (os.path.basename(f), sub_file.read(), "application/octet-stream"),
                )
            )

    return requests.post(
        url, data=data, files=sub_files, cookies=cookies, headers=_HEADERS
    )


def getUrl(cfg, option, default):
    if cfg.has_option("kattis", option):
        return cfg.get("kattis", option)
    else:
        return "https://%s/%s" % (cfg.get("kattis", "hostname"), default)

