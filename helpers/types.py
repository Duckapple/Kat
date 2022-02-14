import re

from helpers.config import getConfig, getConfigUrl


def problem(problemName: str):
    if problemName.startswith(".\\"):
        problemName = problemName[2:]
    if problemName.endswith("\\"):
        problemName = problemName[:-1]
    if len(problemName) == 1:
        section = getConfig().get('contest')
        if problemName in section:
            return section[problemName]
    return problemName


def problemList(lst: list[str] | str):
    if type(lst) == str:
        return problem(lst)
    return [problem(x) for x in lst]


def definedContest(contest_id):
    if re.search('https://.+/(contests|sessions)/\w+', contest_id):
        return contest_id
    id = contest_id.split('/')[-1]
    contestsUrl = getConfigUrl("contestsurl", "contests")
    return f'{contestsUrl}/{id}'