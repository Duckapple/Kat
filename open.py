import webbrowser


def openCommand(problemName):
    url = "https://open.kattis.com/problems/" + problemName
    webbrowser.open(url)

