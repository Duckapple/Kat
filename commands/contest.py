from argparse import ArgumentParser
from helpers.timeutils import toDatetime, toTimeDelta
from commands.submit import submitCommand
from helpers.cli import yes

from bs4 import BeautifulSoup
from helpers.config import getConfig, saveConfig

import requests
from commands.get import getCommand
import string

from helpers.types import definedContest


def contestCommand(data):
    session = requests.Session()
    contestData = readContest(data.get('contest-id'), session)
    if not contestData.get('inProgress'):
        timeTo = contestData.get('timeTo')
        if timeTo and timeTo.total_seconds() > 0:
            print('Contest is not in progress.')
            print(f'Contest begins in {timeTo}.')
            return
        else:
            print('The contest seems to be over.')
            if len(contestData.get('problems')) > 0:
                print('Do you want to get the problems from the contest anyways?')
                if not yes():
                    return
    solved = getCommand({
        **data,
        'command': 'get',
        'problem': contestData.get('problems'),
    })
    #update config with new problems
    config = getConfig()
    config['contest'] = contestData['problemMap']
    saveConfig()


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
    response = session.get(contest)
    body = response.content.decode("utf-8")
    soup = BeautifulSoup(body, "html.parser")
    info = soup.select("#standings thead tr")
    if len(info) != 1:
        print(contest)
        raise Exception("This contest somehow doesn't have a table with a header")

    timeTo = toTimeDelta(soup.select_one(".notstarted .countdown").text)
    remaining = toTimeDelta(soup.select_one(".count_remaining").text)

    # God dammit I hate XML crawling
    endTime = soup.select_one(".contest-progress .text-right").text.strip().split('\n')[1].strip()
    startTime = soup.select_one(".contest-progress .text-left").text.strip().split('\n')[1].strip()

    problemTags = info[0].select(".problemcolheader-standings a")
    if len(problemTags) > 0:
        problems = []
        for problemTag in problemTags:
            problem = problemTag.get('href').split('/')[-1]
            problems.append(problem)

    return {
        'problems': problems,
        'problemMap': {string.ascii_lowercase[i]: x for i, x in enumerate(problems)},
        'inProgress': ((not timeTo) or timeTo <= toTimeDelta("0:00:00")) and (remaining != toTimeDelta("0:00:00")),
        'timeTo': timeTo,
        'remaining': remaining,
        'startTime': toDatetime(startTime),
        'endTime': toDatetime(endTime),
    }


def contestParser(parsers):
    helpText = 'Start kattis contest.'
    description = f"""{helpText} Download all problems from kattis contest, optionally submit any that you have already
                      solved, and allow submitting by using the contest letters as IDs. If contest has not started yet
                      wait until it starts."""
    parser: ArgumentParser = parsers.add_parser('contest', description=description, help=helpText)
    parser.add_argument('contest-id', help='Override the contest to operate on.', type=definedContest)
    parser.add_argument('-s', '--submit', action='store_true', help='Automatically submit pre-solved problems.')