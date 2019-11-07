import requests
def checkProblemExistence(problemName):
    problemUrl = "https://open.kattis.com/problems/" + problemName
    existenceTest = requests.get(problemUrl)
    if existenceTest.status_code != 200:
        raise InvalidProblemException("⚠️ Problem '" + problemName + "' does not exist!")
