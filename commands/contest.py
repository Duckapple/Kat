import time
from argparse import ArgumentParser
from helpers.timeutils import toDatetime, toTimeDelta
from helpers.webutils import getProblemUrl
from commands.submit import submitCommand
from helpers.cli import yes

from bs4 import BeautifulSoup
from helpers.config import getConfig, saveConfig

import requests
from commands.get import getCommand
import string
from enum import Enum


from helpers.types import definedContest


def contestCommand(data):
    session = requests.Session()
    contest = data.get('contest-id')
    contestData = readContest(contest, session)

    if data.get('dump') and not contestData.get('timeState') == TimeState.NotStarted:
        print("Dumping problem links in markdown")
        problems = contestData.get('problems')
        for p in problems:
            print(f"[{p}]({getProblemUrl(p)})")
        return

    if contestData.get('timeState') == TimeState.NotStarted:
        timeTo = contestData.get('timeTo')
        print('Contest has not started yet.')
        print(f'Contest begins in {timeTo}.')
        print("Do you want to run this command again when the contest starts?")
        if not yes():
            return
        print("Waiting for contest to start...")
        while contestData.get('timeState') == TimeState.NotStarted:
            timeTo = contestData.get('timeTo')
            # the -1 denotes that we don't know how long it is to contest start, and will result in the code checking every second
            timeToInSeconds = timeTo.total_seconds() if timeTo is not None else -1
            if timeToInSeconds > 10:
                time.sleep(timeToInSeconds - 10)
            else:
                time.sleep(1)
            contestData = readContest(contest, session)

    elif contestData.get('timeState') == TimeState.Ended:
        print('The contest seems to be over.')
        if len(contestData.get('problems')) > 0:
            print('Do you want to get the problems from the contest anyways?')
            if not yes():
                return
    solved = getCommand({
        **data,
        'command': 'get',
        'problem': contestData.get('problems'),
        'language': None,
    })
    # update config with new problems
    config = getConfig()
    config['contest'] = {
        **contestData['problemMap'],
        "contest": contest
    }
    saveConfig()

    if solved:
        if not data.get('submit'):
            print("Some problems were unarchived from the .solved folder:")
            print(", ".join(solved))
            print("Do you want to submit them?")
            if not yes():
                return
        for problem in solved:
            submitCommand({"problem": problem, "force": True, "archive": True})


class TimeState(Enum):
    NotStarted = 1
    InProgress = 2
    Ended = 3


def readContest(contest, session):
    problems = []
    response = session.get(contest + "/standings")
    body = response.content.decode("utf-8")
    soup = BeautifulSoup(body, "html.parser")
    info = soup.select(".standings-table thead tr")
    print()
    if len(info) != 1:
        print(contest)
        raise Exception(
            "This contest somehow doesn't have a table with a header")

    # check when the contest is/was
    timeState = TimeState.Ended
    timeToText = soup.select_one(".notstarted .countdown").text
    while len(timeToText.split(":")) < 3:
        timeToText = "00:" + timeToText
    timeTo = toTimeDelta(timeToText)
    remaining = toTimeDelta(soup.select_one(".count_remaining").text)
    sessionHasNotStarted = soup.select_one(".count_elapsed").text == "0:00:00"
    sessionHasEnded = soup.select_one(".count_remaining").text == "0:00:00"

    if (timeTo is not None and timeTo > toTimeDelta("0:00:00")) or sessionHasNotStarted:
        timeState = TimeState.NotStarted
    elif (remaining is not None and remaining != toTimeDelta('0:00:00')) or not sessionHasNotStarted:
        timeState = TimeState.InProgress
    if sessionHasEnded:
        timeState = TimeState.Ended

    # God dammit I hate XML crawling
    # I suspect this will not work if the contest ends on another day.
    endTime = soup.select_one(".contest-end").text.strip().split()[0].strip()
    startTime = soup.select_one(
        ".contest-start").text.strip().split()[1].strip()

    problemTags = info[0].select(".table2-header a")
    if len(problemTags) > 0:
        problems = []
        for problemTag in problemTags:
            problem = problemTag.get('href').split('/')[-1]
            problems.append(problem)

    return {
        'problems': problems,
        'problemMap': {string.ascii_lowercase[i]: x for i, x in enumerate(problems)},
        'timeState': timeState,

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
    parser: ArgumentParser = parsers.add_parser(
        'contest', description=description, help=helpText)
    parser.add_argument(
        'contest-id', help='Override the contest to operate on.', type=definedContest)
    parser.add_argument('-s', '--submit', action='store_true',
                        help='Automatically submit pre-solved problems.')
    parser.add_argument('-d', '--dump', action='store_true',
                        help='Dump info about the problems in markdown')
