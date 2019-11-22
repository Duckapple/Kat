import webbrowser
from helpers.url import makeProblemUrl, makeSubmissionUrl


def webCommand(problemName):
    url = makeProblemUrl(problemName)
    webbrowser.open(url)


def openSubmission(submissionId):
    url = makeSubmissionUrl(submissionId)
    webbrowser.open(url)
