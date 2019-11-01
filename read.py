import requests, sys
from auth import login
from config import getConfig
from bs4 import BeautifulSoup
from open import openCommand


def readCommand(args, options):
    session = requests.Session()
    config = getConfig()
    problemName = args[0]
    url = "https://open.kattis.com/problems/" + problemName

    login(config, session)

    if "open" in options:
        openCommand(problemName)
    else:
        problemText = fetchProblemText(url, options, session)

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