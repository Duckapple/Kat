import requests
import sys
import os
from helpers.auth import login
from helpers.config import getConfig
from bs4 import BeautifulSoup
from tabulate import tabulate
from helpers.url import getProblemsUrl


def listCommand(args, options):
    problems = collectProblems(args, options)

    if "-c" in options:
        print(" ".join([x[0] for x in problems]))
    else:
        tableHeaders = ["Id", "Name", "Difficulty"]
        print(tabulate(problems, tableHeaders, tablefmt="psql"))


def collectProblems(args, options):
    session = requests.Session()
    config = getConfig()
    url = getProblemsUrl()
    parameters = buildParameters(args, options)
    login(config, session)
    problems = fetchProblems(url, parameters, args, session)
    return problems


def buildParameters(args, options):
    parameters = {}

    # Order
    order = selectOne(args, {"easiest", "hardest"})

    if order == "easiest":
        parameters["order"] = "problem_difficulty"
    elif order == "hardest":
        parameters["order"] = "problem_difficulty"
        parameters["dir"] = "desc"

    # Status
    status = intersect(
        args, {"solved", "tried", "untried", "unsolved"}) or None

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


def fetchProblems(url, parameters, args, session):
    response = session.get(url, params=parameters)

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
        print("Can only select on of: '" + (", ".join(haystack)) + "'")
        sys.exit(1)
    else:
        return default


def intersect(list1, list2):
    return set(list1).intersection(set(list2))


listFlags = [
    ("page", True, "1"),
    ("limit", True, "50"),
]
