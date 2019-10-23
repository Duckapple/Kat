import os, requests, zipfile, io, shutil


def get(args, forced):
    if os.path.exists(args[0]) or os.path.exists(".archive/" + args[0]):
        print("⚠️ You have already gotten this problem!")
        return
    problem = "https://open.kattis.com/problems/" + args[0]
    existenceTest = requests.get(problem)
    if existenceTest.status_code != 200:
        print("⚠️ Problem does not exist!")
        return
    print("⬇️  Attempting to download exercise from kattis...")
    r = requests.get(problem + "/file/statement/samples.zip", stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    os.makedirs(args[0])
    z.extractall(args[0] + "/test")
    shutil.copy2(
        os.path.dirname(os.path.realpath(__file__)) + "/boilerplate.py",
        args[0] + "/" + args[0] + ".py",
    )
    print("👍 Successfully initialized exercise", args[0] + "!")
    print("   You can test your script with 'kattis test " + args[0] + "'")


def promptToGet(args, options):
    print("This problem is not present...")
    print("Do you want to get it?")
    if yes():
        print("Getting problem...")
        get(args, options)


def yes():
    answer = input("(y/N): ").lower()
    return answer == "y" or answer == "yes"
