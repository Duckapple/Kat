from helpers.config import getConfig


def makeKattisUrl(path):
    cfg = getConfig()
    hostname = cfg.get("kattis", "hostname")
    return "https://"+hostname+path


def makeProblemUrl(problemName):
    return makeKattisUrl("/problems/"+problemName)


def makeSubmissionUrl(id):
    return makeKattisUrl("/submissions/" + id)


def getProblemsUrl():
    return makeKattisUrl("/problems/")
