import glob, os, random
from playsound import playsound

pathToHere = os.path.dirname(os.path.realpath(__file__))
indexOfTrim = pathToHere.index("helpers")
prefix = os.path.join(pathToHere[:indexOfTrim], 'resources')


def winsound():
    playsound(random.choice(glob.glob(os.path.join(prefix, "win", "*.mp3"))))


def losesound():
    playsound(random.choice(glob.glob(os.path.join(prefix, "lose", "*.mp3"))))