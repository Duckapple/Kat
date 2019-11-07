import requests
from helpers.auth import login
from helpers.config import getConfig
from bs4 import BeautifulSoup
from commands.open import openCommand
from helpers.webutils import checkProblemExistence


def readCommand(arg, options):
    session = requests.Session()
    config = getConfig()
    problemName = arg
    problemUrl = "https://open.kattis.com/problems/" + problemName

    checkProblemExistence(problemName)

    if "open" in options:
        openCommand(problemName)
    else:
        problemText = fetchProblemText(problemUrl, options, session)

        for line in problemText:
            print(line)


def addNewlines(textLines):
    result = [""]
    for line in textLines:
        result.append(line)
        result.append("")
    return result


def fetchProblemText(url, options, session):
    response = session.get(url)

    body = response.content.decode("utf-8")
    soup = BeautifulSoup(body, "html.parser")
    headline = soup.select_one(".headline-wrapper h1")
    problem = soup.select_one(".problembody")

    textLines = [headline.text, problem.text]

    textLines = addNewlines(textLines)

    return textLines

readFlags = [
    ("open", False),
]