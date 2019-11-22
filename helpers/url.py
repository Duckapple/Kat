from helpers.config import getConfig


def _makeKattisUrl(path):
    cfg = getConfig()
    hostname = cfg.get("kattis", "hostname")
    return "https://"+hostname+path


def makeProblemUrl(problemName):
    return _makeKattisUrl("/problems/"+problemName)


def makeSubmissionUrl(id):
    return _makeKattisUrl("/submissions/" + id)


def getProblemsUrl():
    return _makeKattisUrl("/problems/")
