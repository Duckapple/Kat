from argparse import ArgumentParser
from commands.submit import submitCommand
from helpers.cli import yes

from bs4 import BeautifulSoup
from helpers.config import getConfigUrl
import re

import requests
from commands.get import getCommand, getFlags

def contestCommand(data):
    session = requests.Session()
    command = data.get('contest_command')

    if command == 'get':
        read = readContest(data.get('contest'), session)
        solved = getCommand({ 
            **data,
            'command': 'get',
            'problem': read.get('problems'),
        })
        if solved:
            if not data.get('submit'):
                print("Some problems were unarchived from the .solved folder:")
                print(", ".join(solved))
                print("Do you want to submit them?")
                if not yes():
                    return
            for problem in solved:
                submitCommand({"problem": problem})

def readContest(contest, session):
    problems = []
    inProgress = False
    timeTo, endTime = None, None
    response = session.get(contest)
    body = response.content.decode("utf-8")
    soup = BeautifulSoup(body, "html.parser")
    info = soup.select("#standings thead tr")
    if len(info) != 1:
        print(contest)
        raise Exception("This contest somehow doesn't have a table with a header")

    timeTo = soup.select_one(".notstarted .countdown").text
    endTime = soup.select_one(".contest-progress .text-right").text

    problemTags = info[0].select(".problemcolheader-standings a")
    if len(problemTags) > 0:
        problems = []
        inProgress = True
        for problemTag in problemTags:
            problem = problemTag.get('href').split('/')[-1]
            problems.append(problem)

    return {
        'problems': problems,
        'inProgress': inProgress,
        'timeTo': timeTo,
        'endTime': endTime,
    }

def definedContest(contest_id):
    if re.search('https://.+/(contests|sessions)/\w+', contest_id):
        return contest_id
    id = contest_id.split('/')[-1]
    contestsUrl = getConfigUrl("contestsurl", "contests")
    return f'{contestsUrl}/{id}'

def contestParser(parsers):
    helpText = 'Run commands specific to Kattis contests.'
    description = f"{helpText} Use `kattis contest set <contest-id> to "
    parser: ArgumentParser = parsers.add_parser('contest', description=description, help=helpText)
    parser.add_argument('-c', '--contest', help='Override the contest to operate on.', type=definedContest)
    subs = parser.add_subparsers(dest='contest_command', metavar='command')

    getText = 'Get the problems associated with the contest.'
    get = subs.add_parser('get', description=getText, help=getText)
    getFlags(get)
    get.add_argument('-s', '--submit', action='store_true', help='Automatically submit pre-solved problems.')
    # get.add_argument('-s', '--submit', action='store_true', help='Submit automatically any projects which have been tested before.')
    # ge = subs.add_parser('ge', description=getText, help=getText)

    # autoSubmitText = 'Automatically submit any problems which match the contest and has passed tests before.'
    # setText = 'Set the contest in which to compete.'
    # set = subparsers.add_parser('set', description=setText, help=setText)
