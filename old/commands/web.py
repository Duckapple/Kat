import webbrowser


def webCommand(problemName):
    url = "https://open.kattis.com/problems/" + problemName
    webbrowser.open(url)


def openSubmission(submissionId):
    url = "https://open.kattis.com/submissions/" + submissionId
    webbrowser.open(url)

