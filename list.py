import requests, sys
from auth import login
from config import getConfig
from bs4 import BeautifulSoup
from tabulate import tabulate

def listCommand(args, options):
    session = requests.Session()
    config = getConfig()
    url = "https://open.kattis.com/problems/"
    parameters = buildParameters(args, options)

    login(config, session)
    
    problems = fetchProblems(url, parameters, session)

    tableHeaders = ["Id", "Name", "Difficulty"]
    print(tabulate(problems, tableHeaders, tablefmt="grid"))

def buildParameters(args, options):
    parameters = {}

    # Order
    order = selectOne(args, {
        'easiest', 'hardest'
    })

    if(order == "easiest"):
        parameters['order'] = "problem_difficulty"
    elif(order == "hardest"):
        parameters['order'] = "problem_difficulty"
        parameters['dir'] = "desc"

    # Status
    status = intersect(args, {
        'solved', 'tried', 'untried', 'unsolved'
    }) or None

    if(status is not None):
        parameters['show_solved'] = "off"
        parameters['show_tried'] = "off"
        parameters['show_untried'] = "off"

    if("unsolved" in args):
        parameters['show_tried'] = "on"
        parameters['show_untried'] = "on"
    if("solved" in args):
        parameters['show_solved'] = "on"
    if("tried" in args):
        parameters['show_tried'] = "on"
    if("untried" in args):
        parameters['show_untried'] = "on"

    return parameters

def fetchProblems(url, parameters, session):
    response = session.get(url, params=parameters)

    body = response.content.decode("utf-8")
    soup = BeautifulSoup(body, "html.parser")

    rows = soup.select(".problem_list tbody tr")
    problems = []

    for row in rows:
        link = row.select_one('.name_column a')

        problems.append([
            link.get('href').replace("/problems/", ""),
            link.text,
            row.select_one('td:nth-of-type(9)').text
        ])

    return problems


def selectOne(needles, haystack, default = None):
    intersection = intersect(needles, haystack)
    size = len(intersection)

    if(size == 1):
        return list(intersection)[0]
    elif(size > 1):
        print("Can only select on of: '" + (", ".join(haystack)) + "'")
        sys.exit(1)
    else:
        return default

def intersect(list1, list2):
    return set(list1).intersection(set(list2))