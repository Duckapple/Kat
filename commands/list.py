from argparse import ArgumentParser
import requests, sys, os
from helpers.auth import login
from helpers.config import getConfigUrl
from bs4 import BeautifulSoup
from tabulate import tabulate


def listCommand(data):
    problems = collectProblems(data)

    if "compact" in data and data['compact']:
        print(" ".join([x[0] for x in problems]))
    else:
        tableHeaders = ["Id", "Name", "Difficulty"]
        print(tabulate(problems, tableHeaders, tablefmt="psql"))


def collectProblems(data):
    session = requests.Session()
    url = getConfigUrl("problemsurl", "problems")
    parameters = buildParameters(data)
    login(session)
    problems = fetchProblems(url, parameters, data, session)
    return problems


def buildParameters(data):
    parameters = {}
    args = data['args']

    if "easiest" in args:
        parameters["order"] = "problem_difficulty"
    elif "hardest" in args:
        parameters["order"] = "problem_difficulty"
        parameters["dir"] = "desc"

    # Status
    status = intersect(args, {"solved", "tried", "untried", "unsolved"}) or None

    if status is not None:
        parameters["show_solved"] = "off"
        parameters["show_tried"] = "off"
        parameters["show_untried"] = "off"

    if "unsolved" in args:
        parameters["show_tried"] = "on"
        parameters["show_untried"] = "on"
    if "solved" in args:
        parameters["show_solved"] = "on"
    if "tried" in args:
        parameters["show_tried"] = "on"
    if "untried" in args:
        parameters["show_untried"] = "on"

    return parameters


def fetchProblems(url, parameters, data, session):
    response = session.get(url, params=parameters)
    args = data["args"]
    args = args if args else []

    body = response.content.decode("utf-8")
    soup = BeautifulSoup(body, "html.parser")

    rows = soup.select(".problem_list tbody tr")
    problems = []

    for row in rows:
        link = row.select_one(".name_column a")
        pName = link.get("href").replace("/problems/", "")
        if 'unarchived' in args and isArchived(pName):
            continue
        problems.append(
            [
                pName,
                link.text,
                row.select_one("td:nth-of-type(9)").text,
            ]
        )

    return problems

def isArchived(problemName, folder=".archive/"):
    return os.path.exists(folder + problemName)

def selectOne(needles, haystack, default=None):
    intersection = intersect(needles, haystack)
    size = len(intersection)

    if size == 1:
        return list(intersection)[0]
    elif size > 1:
        print("Can only select one of: '" + (", ".join(haystack)) + "'")
        sys.exit(1)
    else:
        return default


def intersect(list1, list2):
    return set(list1).intersection(set(list2))

choices = [
    'easiest', 'hardest', 'unarchived', 'unsolved', 'solved', 'untried', 'tried', 'None'
]

def listParser(parsers: ArgumentParser):
    helpText = 'Get a list of problems from the Kattis instance.'
    parser = parsers.add_parser('list', description=helpText, help=helpText)
    parser.add_argument('-p', '--page', type=int, help='Choose which page of results to show')
    parser.add_argument('-l', '--limit', type=int, help='Choose the length of the list/page to show')
    parser.add_argument('-c', '--compact', action='store_true',  help='Print only a space-seperated list of problems')
    listFlags(parser)

def listFlags(parser):
    parser.add_argument('args', metavar='sorting/filter', help='Define which sorting direction and filters to use. Choices for sorting are "easiest" or "hardest", and choices for filters are "unarchived", "unsolved", "solved", "untried" or "tried"', choices=choices, nargs='*', default='None')