import webbrowser


def openCommand(problemName):
    url = "https://open.kattis.com/problems/" + problemName
    webbrowser.open(url)


def openSubmission(submissionId):
    url = "https://open.kattis.com/submissions/" + submissionId
    webbrowser.open(url)

