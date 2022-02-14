import requests
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from commands.web import webCommand
from helpers.config import getConfigUrl
from helpers.types import problemList
from helpers.webutils import checkProblemExistence

def readCommand(data):
    for problem in data['problem']:
        read(problem, data)

def read(problemName, data):
    session = requests.Session()
    problemUrl = getConfigUrl("problemsurl", "problems") + "/" + problemName

    checkProblemExistence(problemName)

    if "console" in data and data['console']:
        problemText = fetchProblemText(problemUrl, session)

        for line in problemText:
            print(line)
    else:
        webCommand(problemName)


def addNewlines(textLines):
    result = [""]
    for line in textLines:
        result.append(line)
        result.append("")
    return result


def fetchProblemText(url, session):
    response = session.get(url)

    body = response.content.decode("utf-8")
    soup = BeautifulSoup(body, "html.parser")
    headline = soup.select_one(".headline-wrapper h1")
    problem = soup.select_one(".problembody")

    textLines = [headline.text, problem.text]

    textLines = addNewlines(textLines)

    return textLines

def readParser(parsers: ArgumentParser):
    helpText = 'Read a problem in the browser or on the command line.'
    parser = parsers.add_parser('read', description=helpText, help=helpText)
    parser.add_argument('problem', help='The problem to read.', nargs='+', type=problemList)
    parser.add_argument('-c', '--console', action='store_true', help='Opt to print the description in the console.')

readFlags = [
    ("console", False),
]