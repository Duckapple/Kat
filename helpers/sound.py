import glob, os, random

from playsound import playsound
prefix = os.path.dirname(os.path.realpath(__file__)) + '/../resources/'


def winsound():
    playsound(random.choice(glob.glob(prefix + "/win/*.mp3")))


def losesound():
    playsound(random.choice(glob.glob(prefix + "/lose/*.mp3")))
