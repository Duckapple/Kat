import webbrowser
from helpers.config import getConfig, getUrl

def webCommand(problemName):
    url = getUrl(getConfig(), "problemsurl", "problems") + "/" + problemName
    webbrowser.open(url)


def openSubmission(submissionId):
    url = getUrl(getConfig(), "submissionsurl", "submissions") + "/" + submissionId
    webbrowser.open(url)

