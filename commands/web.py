import webbrowser
from helpers.config import getConfigUrl

def webCommand(problemName):
    url = getConfigUrl("problemsurl", "problems") + "/" + problemName
    webbrowser.open(url)


def openSubmission(submissionId):
    url = getConfigUrl("submissionsurl", "submissions") + "/" + submissionId
    webbrowser.open(url)

